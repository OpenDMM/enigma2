from skin import parseColor, componentSizes
from Components.config import config, ConfigClock, ConfigInteger, ConfigSelection, ConfigYesNo, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.ActionMap import ActionMap
from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
from Components.EpgList import Rect
from Components.Sources.Event import Event
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Label import Label
from Screens.Screen import Screen
from Screens.EventView import EventViewSimple
from Screens.TimeDateInput import TimeDateInput
from Screens.TimerEntry import TimerEntry
from Screens.EpgSelection import EPGSelection
from Screens.TimerEdit import TimerSanityConflict
from Screens.MessageBox import MessageBox
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from RecordTimer import RecordTimerEntry, parseEvent, AFTEREVENT
from ServiceReference import ServiceReference
from Tools.LoadPixmap import LoadPixmap
from enigma import eEPGCache, eListbox, gFont, eListboxPythonMultiContent, getDesktop, \
	RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, RT_WRAP, eRect, eTimer

from skin import TemplatedListFonts

from time import localtime, time, mktime, strftime

class EPGList(HTMLComponent, GUIComponent):
	GUI_WIDGET = eListbox
	SKIN_COMPONENT_KEY = "MultiEPGList"
	SKIN_COMPONENT_ICON_HEIGHT = "iconHeight"
	SKIN_COMPONENT_ICON_WIDTH = "iconWidth"

	def __init__(self, selChangedCB=None, timer = None, time_epoch = 120, overjump_empty=True):
		sizes = componentSizes[EPGList.SKIN_COMPONENT_KEY]
		self._iconWidth = sizes.get(EPGList.SKIN_COMPONENT_ICON_WIDTH, 22)
		self._iconHeight = sizes.get(EPGList.SKIN_COMPONENT_ICON_HEIGHT, 21)

		self.cur_event = None
		self.cur_service = None
		self.offs = 0
		self.timer = timer
		self.onSelChanged = [ ]
		if selChangedCB is not None:
			self.onSelChanged.append(selChangedCB)
		GUIComponent.__init__(self)
		self.l = eListboxPythonMultiContent()
		self.l.setItemHeight(54);
		self.l.setBuildFunc(self.buildEntry)
		if overjump_empty:
			self.l.setSelectableFunc(self.isSelectable)
		self.epgcache = eEPGCache.getInstance()
		self.clock_pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/epgclock.png'))
		self.clock_add_pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/epgclock_add.png'))
		self.clock_pre_pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/epgclock_pre.png'))
		self.clock_post_pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/epgclock_post.png'))
		self.clock_prepost_pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, 'skin_default/icons/epgclock_prepost.png'))
		self.time_base = None
		self.time_epoch = time_epoch
		self.list = None
		self.event_rect = None

		self.foreColor = None
		self.foreColorSelected = None
		self.borderColor = None
		self.backColor = 0x586d88
		self.backColorSelected = 0x808080
		self.backColorActive = 0x33aa33
		self.backColorActiveSelected = 0x33ee33
		self.foreColorService = None
		self.backColorService = None

	def applySkin(self, desktop, screen):
		if self.skinAttributes is not None:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "EntryForegroundColor":
					self.foreColor = parseColor(value)
				elif attrib == "EntryForegroundColorSelected":
					self.foreColorSelected = parseColor(value)
				elif attrib == "EntryActiveBackgroundColor":
					self.backColorActive = parseColor(value)
				elif attrib == "EntryActiveBackgroundColorSelected":
					self.backColorActiveSelected = parseColor(value)
				elif attrib == "EntryBorderColor":
					self.borderColor = parseColor(value)
				elif attrib == "EntryBackgroundColor":
					self.backColor = parseColor(value)
				elif attrib == "EntryBackgroundColorSelected":
					self.backColorSelected = parseColor(value)
				elif attrib == "ServiceNameForegroundColor":
					self.foreColorService = parseColor(value)
				elif attrib == "ServiceNameBackgroundColor":
					self.backColorService = parseColor(value)
				elif attrib == "EntryFont":
					self.l.setFont(1, gFont(value.split(";")[0], int(value.split(";")[1])))
				elif attrib == "ServiceFont":
					self.l.setFont(0, gFont(value.split(";")[0], int(value.split(";")[1])))
				else:
					attribs.append((attrib,value))
			self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, screen)

	def isSelectable(self, service, sname, event_list):
		return (event_list and len(event_list) and True) or False

	def setEpoch(self, epoch):
#		if self.cur_event is not None and self.cur_service is not None:
		self.offs = 0
		self.time_epoch = epoch
		self.fillMultiEPG(None) # refill

	def getEventFromId(self, service, eventid):
		event = None
		if self.epgcache is not None and eventid is not None:
			event = self.epgcache.lookupEventId(service.ref, eventid)
		return event

	def moveToService(self,serviceref):
		if serviceref is not None:
			for x in range(len(self.list)):
				if self.list[x][0] == serviceref.toString():
					self.instance.moveSelectionTo(x)
					break
	
	def getIndexFromService(self, serviceref):
		if serviceref is not None:
			for x in range(len(self.list)):
				if self.list[x][0] == serviceref.toString():
					return x
		
	def setCurrentIndex(self, index):
		if self.instance is not None:
			self.instance.moveSelectionTo(index)
	
	def getCurrent(self):
		if self.cur_service is None:
			return ( None, None )
		events = self.cur_service[2]
		refstr = self.cur_service[0]
		if self.cur_event is None or not events or not len(events):
			return ( None, ServiceReference(refstr) )
		event = events[self.cur_event] #(event_id, event_title, begin_time, duration)
		eventid = event[0]
		service = ServiceReference(refstr)
		event = self.getEventFromId(service, eventid)
		return ( event, service )

	def connectSelectionChanged(self, func):
		if not self.onSelChanged.count(func):
			self.onSelChanged.append(func)

	def disconnectSelectionChanged(self, func):
		self.onSelChanged.remove(func)

	def serviceChanged(self):
		cur_sel = self.l.getCurrentSelection()
		if cur_sel:
			self.findBestEvent()

	def findBestEvent(self):
		old_service = self.cur_service  #(service, service_name, events)
		cur_service = self.cur_service = self.l.getCurrentSelection()
		last_time = 0;
		time_base = self.getTimeBase()
		if old_service and self.cur_event is not None:
			events = old_service[2]
			cur_event = events[self.cur_event] #(event_id, event_title, begin_time, duration)
			last_time = cur_event[2]
			if last_time < time_base:
				last_time = time_base
		if cur_service:
			self.cur_event = 0
			events = cur_service[2]
			if events and len(events):
				if last_time:
					best_diff = 0
					best = len(events) #set invalid
					idx = 0
					for event in events: #iterate all events
						ev_time = event[2]
						if ev_time < time_base:
							ev_time = time_base
						diff = abs(ev_time-last_time)
						if (best == len(events)) or (diff < best_diff):
							best = idx
							best_diff = diff
						idx += 1
					if best != len(events):
						self.cur_event = best
			else:
				self.cur_event = None
		self.selEntry(0)

	def selectionChanged(self):
		for x in self.onSelChanged:
			if x is not None:
				x()

	def postWidgetCreate(self, instance):
		instance.setWrapAround(True)
		self.selectionChanged_conn = instance.selectionChanged.connect(self.serviceChanged)
		instance.setContent(self.l)
		tlf = TemplatedListFonts()
		self.l.setFont(0, gFont(tlf.face(tlf.MEDIUM), tlf.size(tlf.MEDIUM)))
		self.l.setFont(1, gFont(tlf.face(tlf.SMALL), tlf.size(tlf.SMALL)))
		self.l.setSelectionClip(eRect(0,0,0,0), False)

	def preWidgetRemove(self, instance):
		self.selectionChanged_conn = None
		instance.setContent(None)

	def recalcEntrySize(self):
		esize = self.l.getItemSize()
		width = esize.width()
		height = esize.height()
		xpos = 0;
		w = width/10*2;
		self.service_rect = Rect(xpos, 0, w-10, height)
		xpos += w;
		w = width/10*8;
		self.event_rect = Rect(xpos, 0, w, height)

	def calcEntryPosAndWidthHelper(self, stime, duration, start, end, width):
		xpos = (stime - start) * width / (end - start)
		ewidth = (stime + duration - start) * width / (end - start)
		ewidth -= xpos;
		if xpos < 0:
			ewidth += xpos;
			xpos = 0;
		if (xpos+ewidth) > width:
			ewidth = width - xpos
		return xpos, ewidth

	def calcEntryPosAndWidth(self, event_rect, time_base, time_epoch, ev_start, ev_duration):
		xpos, width = self.calcEntryPosAndWidthHelper(ev_start, ev_duration, time_base, time_base + time_epoch * 60, event_rect.width())
		return xpos+event_rect.left(), width

	def buildEntry(self, service, service_name, events):
		r1=self.service_rect
		r2=self.event_rect
		res = [ None, MultiContentEntryText(
						pos = (r1.left(),r1.top()),
						size = (r1.width(), r1.height()),
						font = 0, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER,
						text = service_name,
						color = self.foreColorService,
						backcolor = self.backColorService) ]

		if events:
			start = self.time_base+self.offs*self.time_epoch*60
			end = start + self.time_epoch * 60
			left = r2.left()
			top = r2.top()
			width = r2.width()
			height = r2.height()
			foreColor = self.foreColor
			foreColorSelected = self.foreColorSelected
			borderColor = self.borderColor

			now = time()

			for ev in events:  #(event_id, event_title, begin_time, duration)
				rec=ev[2] and self.timer.isInTimer(ev[0], ev[2], ev[3], service)
				xpos, ewidth = self.calcEntryPosAndWidthHelper(ev[2], ev[3], start, end, width)
				if ev[2] < now and now < (ev[2]+ev[3]):
					backColor = self.backColorActive
					backColorSelected = self.backColorActiveSelected
				else:
					backColor = self.backColor
					backColorSelected = self.backColorSelected
				res.append(MultiContentEntryText(
					pos = (left+xpos, top), size = (ewidth, height),
					font = 1, flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER | RT_WRAP,
					text = ev[1], color = foreColor, color_sel = foreColorSelected,
					backcolor = backColor, backcolor_sel = backColorSelected, border_width = 1, border_color = borderColor))
				if rec and ewidth > 23:
					res.append(MultiContentEntryPixmapAlphaTest(
						pos = (left+xpos+ewidth-5-self._iconWidth, top+height-5-self._iconHeight), size = (self._iconWidth, self._iconHeight),
						png = self.getClockPixmap(service, ev[2], ev[3], ev[0]),
						backcolor = backColor,
						backcolor_sel = backColorSelected))
		return res

	def selEntry(self, dir, visible=True):
		cur_service = self.cur_service #(service, service_name, events)
		self.recalcEntrySize()
		valid_event = self.cur_event is not None
		if cur_service:
			update = True
			entries = cur_service[2]
			if dir == 0: #current
				update = False
			elif dir == +1: #next
				if valid_event and self.cur_event+1 < len(entries):
					self.cur_event+=1
				else:
					self.offs += 1
					self.fillMultiEPG(None) # refill
					return True
			elif dir == -1: #prev
				if valid_event and self.cur_event-1 >= 0:
					self.cur_event-=1
				elif self.offs > 0:
					self.offs -= 1
					self.fillMultiEPG(None) # refill
					return True
		if cur_service and valid_event:
			entry = entries[self.cur_event] #(event_id, event_title, begin_time, duration)
			time_base = self.time_base+self.offs*self.time_epoch*60
			xpos, width = self.calcEntryPosAndWidth(self.event_rect, time_base, self.time_epoch, entry[2], entry[3])
			self.l.setSelectionClip(eRect(xpos, 0, width, self.event_rect.height()), visible and update)
		else:
			self.l.setSelectionClip(eRect(self.event_rect.left(), self.event_rect.top(), self.event_rect.width(), self.event_rect.height()), False)
		self.selectionChanged()
		return False

	def queryEPG(self, list, buildFunc=None):
		if self.epgcache is not None:
			if buildFunc is not None:
				return self.epgcache.lookupEvent(list, buildFunc)
			else:
				return self.epgcache.lookupEvent(list)
		return [ ]

	def fillMultiEPG(self, services, stime=-1):
		if services is None:
			time_base = self.time_base+self.offs*self.time_epoch*60
			test = [ (service[0], 0, time_base, self.time_epoch) for service in self.list ]
		else:
			self.cur_event = None
			self.cur_service = None
			self.time_base = int(stime)
			test = [ (service.ref.toString(), 0, self.time_base, self.time_epoch) for service in services ]
		test.insert(0, 'XRnITBD')
#		print "BEFORE:"
#		for x in test:
#			print x
		epg_data = self.queryEPG(test)
#		print "EPG:"
#		for x in epg_data:
#			print x
		self.list = [ ]
		tmp_list = None
		service = ""
		sname = ""
		for x in epg_data:
			if service != x[0]:
				if tmp_list is not None:
					self.list.append((service, sname, tmp_list[0][0] is not None and tmp_list or None))
				service = x[0]
				sname = x[1]
				tmp_list = [ ]
			tmp_list.append((x[2], x[3], x[4], x[5]))
		if tmp_list and len(tmp_list):
			self.list.append((service, sname, tmp_list[0][0] is not None and tmp_list or None))

		self.l.setList(self.list)
		self.findBestEvent()

	def getEventRect(self):
		rc = self.event_rect
		return Rect( rc.left() + (self.instance and self.instance.position().x() or 0), rc.top(), rc.width(), rc.height() )

	def getTimeEpoch(self):
		return self.time_epoch

	def getTimeBase(self):
		return self.time_base + (self.offs * self.time_epoch * 60)

	def resetOffset(self):
		self.offs = 0
	
	def getClockPixmap(self, refstr, beginTime, duration, eventId):
		pre_clock = 1
		post_clock = 2
		clock_type = 0
		endTime = beginTime + duration
		for x in self.timer.timer_list:
			if x.service_ref.ref.toString() == refstr:
				if x.eit == eventId:
					return self.clock_pixmap
				beg = x.begin
				end = x.end
				if beginTime > beg and beginTime < end and endTime > end:
					clock_type |= pre_clock
				elif beginTime < beg and endTime > beg and endTime < end:
					clock_type |= post_clock
		if clock_type == 0:
			return self.clock_add_pixmap
		elif clock_type == pre_clock:
			return self.clock_pre_pixmap
		elif clock_type == post_clock:
			return self.clock_post_pixmap
		else:
			return self.clock_prepost_pixmap

	def rebuild(self):
		self.l.setList(self.list)


class TimelineText(HTMLComponent, GUIComponent):
	def __init__(self):
		GUIComponent.__init__(self)
		sizes = componentSizes[componentSizes.TIMELINE_TEXT]
		height = sizes.get(componentSizes.ITEM_HEIGHT, 25)
		self.l = eListboxPythonMultiContent()
		self.l.setSelectionClip(eRect(0, 0, 0, 0))
		self.l.setItemHeight(height);
		tlf = TemplatedListFonts()
		self.l.setFont(0, gFont(tlf.face(tlf.MEDIUM), tlf.size(tlf.MEDIUM)))

	GUI_WIDGET = eListbox

	def applySkin(self, desktop, screen):
		if self.skinAttributes is not None:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "TimelineFont":
					self.l.setFont(0, gFont(value.split(";")[0], int(value.split(";")[1])))
				else:
					attribs.append((attrib,value))
			self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, screen)

	def postWidgetCreate(self, instance):
		instance.setContent(self.l)

	def setEntries(self, entries):
		sizes = componentSizes[componentSizes.TIMELINE_TEXT]
		width = sizes.get(componentSizes.ITEM_WIDTH, 60)
		height = sizes.get(componentSizes.ITEM_HEIGHT, 25)
		res = [ None ] # no private data needed
		for x in entries:
			tm = x[0]
			xpos = x[1]
			txt = strftime("%H:%M", localtime(tm))
			res.append((eListboxPythonMultiContent.TYPE_TEXT, xpos-30, 0, width, height, 0, RT_HALIGN_CENTER|RT_VALIGN_CENTER, txt))
		self.l.setList([res])

config.misc.graph_mepg_prev_time=ConfigClock(default = time())
config.misc.graph_mepg_prev_time_period=ConfigInteger(default=120, limits=(60,300))

now = [x for x in localtime()]
now[3] = 20
now[4] = 15
def_time = mktime(now)
config.misc.graph_mepg_prime_time=ConfigClock(default=def_time)
config.misc.graph_mepg_current_service=ConfigYesNo(default=True)

okChoices = [ ("zap", _("Zap")), ("info", _("Info")) ]
config.misc.graph_mepg_ok_button=ConfigSelection(okChoices, default = "zap")

class GraphMultiEPG(Screen):
	EMPTY = 0
	ADD_TIMER = 1
	REMOVE_TIMER = 2
	
	ZAP = 1

	TIME_NOW = 0
	TIME_PRIME = 1

	def __init__(self, session, services, zapFunc=None, bouquetChangeCB=None):
		Screen.__init__(self, session)
		self.bouquetChangeCB = bouquetChangeCB
		now = time()
		tmp = now % 900
		self.ask_time = now - tmp
		self.closeRecursive = False
		self["key_red"] = Button("")
		self["key_green"] = Button("")
		self["key_yellow"] = Button(_("Prime time"))
		self["key_blue"] = Button(_("Date"))
		self.key_green_choice = self.EMPTY
		self.key_red_choice = self.EMPTY
		self["timeline_text"] = TimelineText()
		self["Event"] = Event()
		self.time_lines = [ ]
		for x in (0,1,2,3,4,5):
			pm = Pixmap()
			self.time_lines.append(pm)
			self["timeline%d"%(x)] = pm
		self["timeline_now"] = Pixmap()
		self.services = services
		self.zapFunc = zapFunc
		self.prime_mode = self.TIME_NOW

		self["list"] = EPGList(selChangedCB = self.onSelectionChanged, timer = self.session.nav.RecordTimer, time_epoch = config.misc.graph_mepg_prev_time_period.value )

		self["actions"] = ActionMap(["EPGSelectActions", "OkCancelActions"],
			{
				"cancel": self.closeScreen,
				"ok": self.okKeyPressed,
				"timerAdd": self.timerAdd,
				"info": self.infoKeyPressed,
				"red": self.zapTo,
				"yellow": self.primeTime,
				"blue" : self.enterDateTime,
				"input_date_time": self.configMenu,
				"nextBouquet": self.nextBouquet,
				"prevBouquet": self.prevBouquet,
			})
		self["actions"].csel = self

		self["input_actions"] = ActionMap(["InputActions"],
			{
				"left": self.leftPressed,
				"right": self.rightPressed,
				"1": self.key1,
				"2": self.key2,
				"3": self.key3,
				"4": self.key4,
				"5": self.key5,
			},-1)

		self.updateTimelineTimer = eTimer()
		self.updateTimelineTimer_conn = self.updateTimelineTimer.timeout.connect(self.moveTimeLines)
		self.updateTimelineTimer.start(60*1000)
		self.onLayoutFinish.append(self.onCreate)

	def leftPressed(self):
		self.prevEvent()

	def rightPressed(self):
		self.nextEvent()

	def nextEvent(self, visible=True):
		ret = self["list"].selEntry(+1, visible)
		if ret:
			self.moveTimeLines(True)

	def prevEvent(self, visible=True):
		ret = self["list"].selEntry(-1, visible)
		if ret:
			self.moveTimeLines(True)

	def key1(self):
		self["list"].setEpoch(60)
		config.misc.graph_mepg_prev_time_period.value = 60
		self.moveTimeLines()

	def key2(self):
		self["list"].setEpoch(120)
		config.misc.graph_mepg_prev_time_period.value = 120
		self.moveTimeLines()

	def key3(self):
		self["list"].setEpoch(180)
		config.misc.graph_mepg_prev_time_period.value = 180
		self.moveTimeLines()

	def key4(self):
		self["list"].setEpoch(240)
		config.misc.graph_mepg_prev_time_period.value = 240
		self.moveTimeLines()

	def key5(self):
		self["list"].setEpoch(300)
		config.misc.graph_mepg_prev_time_period.value = 300
		self.moveTimeLines()

	def nextBouquet(self):
		if self.bouquetChangeCB:
			self.bouquetChangeCB(1, self)
			self["list"].setCurrentIndex(0)

	def prevBouquet(self):
		if self.bouquetChangeCB:
			self.bouquetChangeCB(-1, self)
			self["list"].setCurrentIndex(0)

	def configMenu(self):
		self.session.open(GraphMultiEPGMenu)

	def enterDateTime(self):
		self.session.openWithCallback(self.onDateTimeInputClosed, TimeDateInput, config.misc.graph_mepg_prev_time )

	def onDateTimeInputClosed(self, ret):
		if len(ret) > 1:
			if ret[0]:
				self.ask_time=ret[1]
				l = self["list"]
				l.resetOffset()
				l.fillMultiEPG(self.services, ret[1])
				self.moveTimeLines(True)

	def primeTime(self):
		date = time()
		if self.prime_mode == self.TIME_NOW:
			now = [x for x in localtime()]
			prime =  [y for y in config.misc.graph_mepg_prime_time.value]
			date = mktime([now[0], now[1], now[2], prime[0], prime[1], 0, 0, 0, -1])
			if now[3] > prime[0] or (now[3] == prime[0] and now[4] > prime[1]):
				date = date + 60*60*24;
			self["key_yellow"].setText(_("Now"))
			self.prime_mode = self.TIME_PRIME
		else:
			tmp = date % 900
			date = date - tmp
			self["key_yellow"].setText(_("Prime time"))
			self.prime_mode = self.TIME_NOW

		self.ask_time = date
		l = self["list"]
		l.resetOffset()
		l.fillMultiEPG(self.services, date)
		self.moveTimeLines(True)

	def closeScreen(self):
		self.close(self.closeRecursive)

	def infoKeyPressed(self):
		cur = self["list"].getCurrent()
		event = cur[0]
		service = cur[1]
		if event is not None:
			self.session.open(EventViewSimple, event, service, self.eventViewCallback, self.openSimilarList)

	def openSimilarList(self, eventid, refstr):
		self.session.open(EPGSelection, refstr, None, eventid)

	def setServices(self, services):
		self.services = services
		self.onCreate()

	#just used in multipeg
	def onCreate(self):
		self["list"].fillMultiEPG(self.services, self.ask_time)
		if config.misc.graph_mepg_current_service.value:
			self["list"].moveToService(self.session.nav.getCurrentlyPlayingServiceReference())
		self.moveTimeLines()

	def eventViewCallback(self, setEvent, setService, val):
		l = self["list"]
		old = l.getCurrent()
		if val == -1:
			self.prevEvent(False)
		elif val == +1:
			self.nextEvent(False)
		cur = l.getCurrent()
		if cur[0] is None and cur[1].ref != old[1].ref:
			self.eventViewCallback(setEvent, setService, val)
		else:
			setService(cur[1])
			setEvent(cur[0])

	def zapTo(self):
		if self.zapFunc and self.key_red_choice == self.ZAP:
			self.closeRecursive = True
			ref = self["list"].getCurrent()[1]
			if ref:
				self.zapFunc(ref.ref)

	#for backwardscompat in (maybe someone derived his stuff from this?!)
	def eventSelected(self):
		self.okKeyPressed()

	def okKeyPressed(self):
		if config.misc.graph_mepg_ok_button.value == "zap":
			self.zapTo()
		elif config.misc.graph_mepg_ok_button.value == "info":
			self.infoKeyPressed()

	def removeTimer(self, timer):
		timer.afterEvent = AFTEREVENT.NONE
		self.session.nav.RecordTimer.removeEntry(timer)
		self["key_green"].setText(_("Add timer"))
		self.key_green_choice = self.ADD_TIMER
		self["list"].rebuild()

	def timerAdd(self):
		cur = self["list"].getCurrent()
		event = cur[0]
		serviceref = cur[1]
		if event is None:
			return
		eventid = event.getEventId()
		refstr = serviceref.ref.toString()
		for timer in self.session.nav.RecordTimer.timer_list:
			if timer.eit == eventid and timer.service_ref.ref.toString() == refstr:
				cb_func = lambda ret : not ret or self.removeTimer(timer)
				self.session.openWithCallback(cb_func, MessageBox, _("Do you really want to delete %s?") % event.getEventName())
				break
		else:
			newEntry = RecordTimerEntry(serviceref, checkOldTimers = True, *parseEvent(event))
			self.session.openWithCallback(self.finishedAdd, TimerEntry, newEntry)

	def finishedAdd(self, answer):
		print "finished add"
		if answer[0]:
			entry = answer[1]
			simulTimerList = self.session.nav.RecordTimer.record(entry)
			if simulTimerList is not None:
				for x in simulTimerList:
					if x.setAutoincreaseEnd(entry):
						self.session.nav.RecordTimer.timeChanged(x)
				simulTimerList = self.session.nav.RecordTimer.record(entry)
				if simulTimerList is not None:
					self.session.openWithCallback(self.finishSanityCorrection, TimerSanityConflict, simulTimerList)
			self["key_green"].setText(_("Remove timer"))
			self.key_green_choice = self.REMOVE_TIMER
		else:
			self["key_green"].setText(_("Add timer"))
			self.key_green_choice = self.ADD_TIMER
			print "Timeredit aborted"
	
	def finishSanityCorrection(self, answer):
		self.finishedAdd(answer)

	def onSelectionChanged(self):
		cur = self["list"].getCurrent()
		if cur is None:
			if self.key_green_choice != self.EMPTY:
				self["key_green"].setText("")
				self.key_green_choice = self.EMPTY
			if self.key_red_choice != self.EMPTY:
				self["key_red"].setText("")
				self.key_red_choice = self.EMPTY
			return
		
		event = cur[0]
		self["Event"].newEvent(event)
		
		if cur[1] is None or cur[1].getServiceName() == "":
			if self.key_green_choice != self.EMPTY:
				self["key_green"].setText("")
				self.key_green_choice = self.EMPTY
			if self.key_red_choice != self.EMPTY:
				self["key_red"].setText("")
				self.key_red_choice = self.EMPTY
			return
		elif self.key_red_choice != self.ZAP:
				self["key_red"].setText("Zap")
				self.key_red_choice = self.ZAP
			
		if not event:
			if self.key_green_choice != self.EMPTY:
				self["key_green"].setText("")
				self.key_green_choice = self.EMPTY
			return
		
		serviceref = cur[1]
		eventid = event.getEventId()
		refstr = serviceref.ref.toString()
		isRecordEvent = False
		for timer in self.session.nav.RecordTimer.timer_list:
			if timer.eit == eventid and timer.service_ref.ref.toString() == refstr:
				isRecordEvent = True
				break
		if isRecordEvent and self.key_green_choice != self.REMOVE_TIMER:
			self["key_green"].setText(_("Remove timer"))
			self.key_green_choice = self.REMOVE_TIMER
		elif not isRecordEvent and self.key_green_choice != self.ADD_TIMER:
			self["key_green"].setText(_("Add timer"))
			self.key_green_choice = self.ADD_TIMER
	
	def moveTimeLines(self, force=False):
		self.updateTimelineTimer.start((60-(int(time())%60))*1000)	#keep syncronised
		l = self["list"]
		event_rect = l.getEventRect()
		time_epoch = l.getTimeEpoch()
		time_base = l.getTimeBase()
		if event_rect is None or time_epoch is None or time_base is None:
			return
		time_steps = time_epoch > 180 and 60 or 30
		
		num_lines = time_epoch/time_steps
		incWidth=event_rect.width()/num_lines
		pos=event_rect.left()
		timeline_entries = [ ]
		x = 0
		changecount = 0
		for line in self.time_lines:
			old_pos = line.position
			new_pos = (x == num_lines and event_rect.left()+event_rect.width() or pos, old_pos[1])
			if not x or x >= num_lines:
				line.visible = False
			else:
				if old_pos != new_pos:
					line.setPosition(new_pos[0], new_pos[1])
					changecount += 1
				line.visible = True
			if not x or line.visible:
				timeline_entries.append((time_base + x * time_steps * 60, new_pos[0]))
			x += 1
			pos += incWidth

		if changecount or force:
			self["timeline_text"].setEntries(timeline_entries)

		now=time()
		timeline_now = self["timeline_now"]
		if now >= time_base and now < (time_base + time_epoch * 60):
			xpos = int((((now - time_base) * event_rect.width()) / (time_epoch * 60))-(timeline_now.instance.size().width()/2))
			old_pos = timeline_now.position
			new_pos = (xpos+event_rect.left(), old_pos[1])
			if old_pos != new_pos:
				timeline_now.setPosition(new_pos[0], new_pos[1])
			timeline_now.visible = True
		else:
			timeline_now.visible = False
		# here no l.l.invalidate() is needed when the zPosition in the skin is correct!

# ----------------------------------------

HELP_TEXT_PRIME_TIME      = _("Time to jump to by pressing the yellow key.")
HELP_TEXT_CURRENT_SERVICE = _("Start with current service instead of first service.")
HELP_TEXT_OK_BUTTON       = _("Select your favorite mapping.")

class GraphMultiEPGMenu(ConfigListScreen, Screen):
	IS_DIALOG = True
	onChangedEntry = [ ]

	def __init__(self, session):
		width = 492
		height = 230
		dsk_size   = getDesktop(0).size()
		left = (dsk_size.width() - width)>>1
		top = (dsk_size.height() - height)>>1
		GraphMultiEPGMenu.skin = """<screen position="%d,%d" size="%d,%d" title="%s">
				<widget name="config" position="0,0"   size="492,105" scrollbarMode="showOnDemand" zPosition="1"/>
				<ePixmap pixmap="skin_default/div-h.png" position="0,108" zPosition="1" size="492,2" />
				<widget name="label"  position="0,110" size="492,70" font="Regular;16" zPosition="1" halign="left" valign="top"/>
				<ePixmap pixmap="skin_default/div-h.png" position="0,185" zPosition="1" size="492,2" />
				<ePixmap pixmap="skin_default/buttons/red.png"    position="0,190"   zPosition="0" size="140,40" transparent="1" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/green.png"  position="176,190" zPosition="0" size="140,40" transparent="1" alphatest="on" />
				<ePixmap pixmap="skin_default/buttons/yellow.png" position="352,190" zPosition="0" size="140,40" transparent="1" alphatest="on" />
				<widget name="key_r" position="0,190"   size="140,40" zPosition="5" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
				<widget name="key_g" position="176,190" size="140,40" zPosition="5" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
				<widget name="key_y" position="352,190" size="140,40" zPosition="5" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />
			</screen>""" % (left, top, width, height, _("GraphMultiEPG settings"))

		Screen.__init__(self, session)

		# create config list
		self.list = []
		ConfigListScreen.__init__(self, self.list)
		self.createConfigList()

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"ok"     : self.okPressed,
			"cancel" : self.cancelPressed,
			"red"    : self.cancelPressed,
			"green"  : self.okPressed,
			"yellow" : self.resetPressed,
			"menu"   : self.cancelPressed,
		}, -2)
		self["actions"].setEnabled(True)

		self["label"] = Label("Info")
		self["key_r"] = Label(_("Cancel"))
		self["key_y"] = Label(_("Default"))
		self["key_g"] = Label(_("OK"))
		self.onLayoutFinish.append(self.__layoutFinished)

	def __layoutFinished(self):
		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def selectionChanged(self):
		elem = self["config"].getCurrent()[1]
		if elem == config.misc.graph_mepg_prime_time:
			self["label"].setText(HELP_TEXT_PRIME_TIME)
		elif elem == config.misc.graph_mepg_current_service:
			self["label"].setText(HELP_TEXT_CURRENT_SERVICE)
		elif elem == config.misc.graph_mepg_ok_button:
			self["label"].setText(HELP_TEXT_OK_BUTTON)

	def createConfigList(self):
		# remove notifiers
		for x in self["config"].list:
			x[1].clearNotifiers()

		self.list = [
			getConfigListEntry(_("Prime time"),                 config.misc.graph_mepg_prime_time),
			getConfigListEntry(_("Start with current service"), config.misc.graph_mepg_current_service),
			getConfigListEntry(_("OK button mapping"),          config.misc.graph_mepg_ok_button)
		]
		self["config"].list = self.list

		# add notifiers (lcd, info)
		for x in self["config"].list:
			x[1].addNotifier(self.changedEntry)

	def resetPressed(self):
		global def_time
		now = [x for x in localtime()]
		now[3] = 20
		now[4] = 15
		def_time = mktime(now)
		config.misc.graph_mepg_prime_time.value = [20, 15]
		config.misc.graph_mepg_current_service.value = True
		config.misc.graph_mepg_ok_button.value = "zap"
		self.createConfigList()

	def okPressed(self):
		for x in self["config"].list:
			x[1].save()
		self.close(None)

	def cancelPressed(self):
		confirm = False
		for x in self["config"].list:
			confirm = confirm or x[1].isChanged()
		if confirm:
			self.session.openWithCallback(self._discardConfirm, MessageBox, _("Discard changes?"))
		else:
			self.close(None)

	def _discardConfirm(self, result):
		if result:
			for x in self["config"].list:
				if x[1].isChanged():
					x[1].cancel()
			self.close(None)

	# ---- for summary (lcd) ----
	def changedEntry(self, element=None):
		for x in self.onChangedEntry:
			x()

	def getCurrentEntry(self):
		return self["config"].getCurrent()[0]

	def getCurrentValue(self):
		return "..."

	def createSummary(self):
		return GraphMultiEPGMenuSummary

# ----------------------------------------

class GraphMultiEPGMenuSummary(Screen):

	skin = ("""<screen name="GraphMultiEPGMenuSummary" position="0,0" size="132,64" id="1">
			<widget name="SetupTitle" position="6,4"  size="120,20" font="Regular;20" halign="center"/>
			<widget name="SetupEntry" position="6,30" size="120,12" font="Regular;12" halign="left"/>
			<widget name="SetupValue" position="6,48" size="120,12" font="Regular;12" halign="right"/>
		</screen>""",
		"""<screen name="GraphMultiEPGMenuSummary" position="0,0" size="96,64" id="2">
			<widget name="SetupTitle" position="3,4"  size="90,20" font="Regular;20" halign="center"/>
			<widget name="SetupEntry" position="3,30" size="90,12" font="Regular;12" halign="left"/>
			<widget name="SetupValue" position="3,48" size="90,12" font="Regular;12" halign="right"/>
		</screen>""")

	def __init__(self, session, parent):
		Screen.__init__(self, session, parent = parent)
		self["SetupTitle"] = Label(_("GraphMultiEPG settings"))
		self["SetupEntry"] = Label("")
		self["SetupValue"] = Label("")
		self.onShow.append(self.addWatcher)
		self.onHide.append(self.removeWatcher)

	def addWatcher(self):
		self.parent.onChangedEntry.append(self.selectionChanged)
		self.parent["config"].onSelectionChanged.append(self.selectionChanged)
		self.selectionChanged()

	def removeWatcher(self):
		self.parent.onChangedEntry.remove(self.selectionChanged)
		self.parent["config"].onSelectionChanged.remove(self.selectionChanged)

	def selectionChanged(self):
		self["SetupEntry"].text = self.parent.getCurrentEntry()
		self["SetupValue"].text = self.parent.getCurrentValue()
