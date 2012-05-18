# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.4
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (3,0,0):
    new_instancemethod = lambda func, inst, cls: _webview.SWIG_PyInstanceMethod_New(func)
else:
    from new import instancemethod as new_instancemethod
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_webview', [dirname(__file__)])
        except ImportError:
            import _webview
            return _webview
        if fp is not None:
            try:
                _mod = imp.load_module('_webview', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _webview = swig_import_helper()
    del swig_import_helper
else:
    import _webview
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


def _swig_setattr_nondynamic_method(set):
    def set_attr(self,name,value):
        if (name == "thisown"): return self.this.own(value)
        if hasattr(self,name) or (name == "this"):
            set(self,name,value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


class iObject(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _webview.delete_iObject
iObject_swigregister = _webview.iObject_swigregister
iObject_swigregister(iObject)


def ptrAssert(*args):
  return _webview.ptrAssert(*args)
ptrAssert = _webview.ptrAssert
MAX_LAYER = _webview.MAX_LAYER
class eWidget(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        _webview.eWidget_swiginit(self,_webview.new_eWidget(*args))
    __swig_destroy__ = _webview.delete_eWidget
    m_animation = _swig_property(_webview.eWidget_m_animation_get, _webview.eWidget_m_animation_set)
    m_clip_region = _swig_property(_webview.eWidget_m_clip_region_get, _webview.eWidget_m_clip_region_set)
    m_visible_region = _swig_property(_webview.eWidget_m_visible_region_get, _webview.eWidget_m_visible_region_set)
    m_visible_with_childs = _swig_property(_webview.eWidget_m_visible_with_childs_get, _webview.eWidget_m_visible_with_childs_set)
    m_comp_buffer = _swig_property(_webview.eWidget_m_comp_buffer_get, _webview.eWidget_m_comp_buffer_set)
    evtPaint = _webview.eWidget_evtPaint
    evtKey = _webview.eWidget_evtKey
    evtChangedPosition = _webview.eWidget_evtChangedPosition
    evtChangedSize = _webview.eWidget_evtChangedSize
    evtParentChangedPosition = _webview.eWidget_evtParentChangedPosition
    evtParentVisibilityChanged = _webview.eWidget_evtParentVisibilityChanged
    evtWillChangePosition = _webview.eWidget_evtWillChangePosition
    evtWillChangeSize = _webview.eWidget_evtWillChangeSize
    evtAction = _webview.eWidget_evtAction
    evtFocusGot = _webview.eWidget_evtFocusGot
    evtFocusLost = _webview.eWidget_evtFocusLost
    evtUserWidget = _webview.eWidget_evtUserWidget
eWidget.move = new_instancemethod(_webview.eWidget_move,None,eWidget)
eWidget.resize = new_instancemethod(_webview.eWidget_resize,None,eWidget)
eWidget.position = new_instancemethod(_webview.eWidget_position,None,eWidget)
eWidget.size = new_instancemethod(_webview.eWidget_size,None,eWidget)
eWidget.csize = new_instancemethod(_webview.eWidget_csize,None,eWidget)
eWidget.invalidate = new_instancemethod(_webview.eWidget_invalidate,None,eWidget)
eWidget.child = new_instancemethod(_webview.eWidget_child,None,eWidget)
eWidget.show = new_instancemethod(_webview.eWidget_show,None,eWidget)
eWidget.hide = new_instancemethod(_webview.eWidget_hide,None,eWidget)
eWidget.destruct = new_instancemethod(_webview.eWidget_destruct,None,eWidget)
eWidget.getStyle = new_instancemethod(_webview.eWidget_getStyle,None,eWidget)
eWidget.setStyle = new_instancemethod(_webview.eWidget_setStyle,None,eWidget)
eWidget.setBackgroundColor = new_instancemethod(_webview.eWidget_setBackgroundColor,None,eWidget)
eWidget.clearBackgroundColor = new_instancemethod(_webview.eWidget_clearBackgroundColor,None,eWidget)
eWidget.setZPosition = new_instancemethod(_webview.eWidget_setZPosition,None,eWidget)
eWidget.setTransparent = new_instancemethod(_webview.eWidget_setTransparent,None,eWidget)
eWidget.isVisible = new_instancemethod(_webview.eWidget_isVisible,None,eWidget)
eWidget.isTransparent = new_instancemethod(_webview.eWidget_isTransparent,None,eWidget)
eWidget.getAbsolutePosition = new_instancemethod(_webview.eWidget_getAbsolutePosition,None,eWidget)
eWidget.event = new_instancemethod(_webview.eWidget_event,None,eWidget)
eWidget.setFocus = new_instancemethod(_webview.eWidget_setFocus,None,eWidget)
eWidget.setPositionNotifyChild = new_instancemethod(_webview.eWidget_setPositionNotifyChild,None,eWidget)
eWidget.notifyShowHide = new_instancemethod(_webview.eWidget_notifyShowHide,None,eWidget)
eWidget_swigregister = _webview.eWidget_swigregister
eWidget_swigregister(eWidget)


def getDesktop(*args):
  return _webview.getDesktop(*args)
getDesktop = _webview.getDesktop
class stdStringArray(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        _webview.stdStringArray_swiginit(self,_webview.new_stdStringArray(*args))
    __swig_destroy__ = _webview.delete_stdStringArray
    frompointer = staticmethod(_webview.stdStringArray_frompointer)
stdStringArray.__getitem__ = new_instancemethod(_webview.stdStringArray___getitem__,None,stdStringArray)
stdStringArray.__setitem__ = new_instancemethod(_webview.stdStringArray___setitem__,None,stdStringArray)
stdStringArray.cast = new_instancemethod(_webview.stdStringArray_cast,None,stdStringArray)
stdStringArray_swigregister = _webview.stdStringArray_swigregister
stdStringArray_swigregister(stdStringArray)

def stdStringArray_frompointer(*args):
  return _webview.stdStringArray_frompointer(*args)
stdStringArray_frompointer = _webview.stdStringArray_frompointer

class PyCaller(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PyCaller_swiginit(self,_webview.new_PyCaller())
    __swig_destroy__ = _webview.delete_PyCaller
PyCaller_swigregister = _webview.PyCaller_swigregister
PyCaller_swigregister(PyCaller)

class PSignal(PyCaller):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PSignal_swiginit(self,_webview.new_PSignal())
    __swig_destroy__ = _webview.delete_PSignal
PSignal.get = new_instancemethod(_webview.PSignal_get,None,PSignal)
PSignal_swigregister = _webview.PSignal_swigregister
PSignal_swigregister(PSignal)


def PyDict_SetItem_DECREF(*args):
  return _webview.PyDict_SetItem_DECREF(*args)
PyDict_SetItem_DECREF = _webview.PyDict_SetItem_DECREF

def PySet_Add_DECREF(*args):
  return _webview.PySet_Add_DECREF(*args)
PySet_Add_DECREF = _webview.PySet_Add_DECREF
class PyConv(object):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    PyFrom = staticmethod(_webview.PyConv_PyFrom)
    def __init__(self): 
        _webview.PyConv_swiginit(self,_webview.new_PyConv())
    __swig_destroy__ = _webview.delete_PyConv
PyConv_swigregister = _webview.PyConv_swigregister
PyConv_swigregister(PyConv)

def PyConv_PyFrom(*args):
  return _webview.PyConv_PyFrom(*args)
PyConv_PyFrom = _webview.PyConv_PyFrom

class PySignalArg(PyCaller):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        _webview.PySignalArg_swiginit(self,_webview.new_PySignalArg(*args))
    __swig_destroy__ = _webview.delete_PySignalArg
PySignalArg_swigregister = _webview.PySignalArg_swigregister
PySignalArg_swigregister(PySignalArg)

class PySignal0(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal0_swiginit(self,_webview.new_PySignal0())
    __swig_destroy__ = _webview.delete_PySignal0
PySignal0.__call__ = new_instancemethod(_webview.PySignal0___call__,None,PySignal0)
PySignal0_swigregister = _webview.PySignal0_swigregister
PySignal0_swigregister(PySignal0)

class PySignal1(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal1_swiginit(self,_webview.new_PySignal1())
    __swig_destroy__ = _webview.delete_PySignal1
PySignal1.__call__ = new_instancemethod(_webview.PySignal1___call__,None,PySignal1)
PySignal1_swigregister = _webview.PySignal1_swigregister
PySignal1_swigregister(PySignal1)

class PySignal2(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal2_swiginit(self,_webview.new_PySignal2())
    __swig_destroy__ = _webview.delete_PySignal2
PySignal2.__call__ = new_instancemethod(_webview.PySignal2___call__,None,PySignal2)
PySignal2_swigregister = _webview.PySignal2_swigregister
PySignal2_swigregister(PySignal2)

class PySignal3(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal3_swiginit(self,_webview.new_PySignal3())
    __swig_destroy__ = _webview.delete_PySignal3
PySignal3.__call__ = new_instancemethod(_webview.PySignal3___call__,None,PySignal3)
PySignal3_swigregister = _webview.PySignal3_swigregister
PySignal3_swigregister(PySignal3)

class PySignal4(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal4_swiginit(self,_webview.new_PySignal4())
    __swig_destroy__ = _webview.delete_PySignal4
PySignal4.__call__ = new_instancemethod(_webview.PySignal4___call__,None,PySignal4)
PySignal4_swigregister = _webview.PySignal4_swigregister
PySignal4_swigregister(PySignal4)

class PySignal5(PSignal):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self): 
        _webview.PySignal5_swiginit(self,_webview.new_PySignal5())
    __swig_destroy__ = _webview.delete_PySignal5
PySignal5.__call__ = new_instancemethod(_webview.PySignal5___call__,None,PySignal5)
PySignal5_swigregister = _webview.PySignal5_swigregister
PySignal5_swigregister(PySignal5)

class eWebView(eWidget):
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    navOpenLink = _webview.eWebView_navOpenLink
    navLeft = _webview.eWebView_navLeft
    navRight = _webview.eWebView_navRight
    navUp = _webview.eWebView_navUp
    navDown = _webview.eWebView_navDown
    navPageUp = _webview.eWebView_navPageUp
    navPageDown = _webview.eWebView_navPageDown
    navHome = _webview.eWebView_navHome
    navEnd = _webview.eWebView_navEnd
    navTab = _webview.eWebView_navTab
    navBackspace = _webview.eWebView_navBackspace
    navBacktab = _webview.eWebView_navBacktab
    navDelete = _webview.eWebView_navDelete
    navRed = _webview.eWebView_navRed
    navGreen = _webview.eWebView_navGreen
    navYellow = _webview.eWebView_navYellow
    navBlue = _webview.eWebView_navBlue
    nav0 = _webview.eWebView_nav0
    nav1 = _webview.eWebView_nav1
    nav2 = _webview.eWebView_nav2
    nav3 = _webview.eWebView_nav3
    nav4 = _webview.eWebView_nav4
    nav5 = _webview.eWebView_nav5
    nav6 = _webview.eWebView_nav6
    nav7 = _webview.eWebView_nav7
    nav8 = _webview.eWebView_nav8
    nav9 = _webview.eWebView_nav9
    navBack = _webview.eWebView_navBack
    navForward = _webview.eWebView_navForward
    navStop = _webview.eWebView_navStop
    navReload = _webview.eWebView_navReload
    def __init__(self, *args): 
        _webview.eWebView_swiginit(self,_webview.new_eWebView(*args))
    __swig_destroy__ = _webview.delete_eWebView
    contentsSizeChanged = _swig_property(_webview.eWebView_contentsSizeChanged_get)
    iconChanged = _swig_property(_webview.eWebView_iconChanged_get)
    initialLayoutCompleted = _swig_property(_webview.eWebView_initialLayoutCompleted_get)
    javaScriptWindowObjectCleared = _swig_property(_webview.eWebView_javaScriptWindowObjectCleared_get)
    pageChanged = _swig_property(_webview.eWebView_pageChanged_get)
    titleChanged = _swig_property(_webview.eWebView_titleChanged_get)
    urlChanged = _swig_property(_webview.eWebView_urlChanged_get)
    contentsChanged = _swig_property(_webview.eWebView_contentsChanged_get)
    downloadRequested = _swig_property(_webview.eWebView_downloadRequested_get)
    geometryChangeRequested = _swig_property(_webview.eWebView_geometryChangeRequested_get)
    linkClicked = _swig_property(_webview.eWebView_linkClicked_get)
    linkHovered = _swig_property(_webview.eWebView_linkHovered_get)
    loadFinished = _swig_property(_webview.eWebView_loadFinished_get)
    loadProgress = _swig_property(_webview.eWebView_loadProgress_get)
    loadStarted = _swig_property(_webview.eWebView_loadStarted_get)
    menuBarVisibilityChangeRequested = _swig_property(_webview.eWebView_menuBarVisibilityChangeRequested_get)
    microFocusChanged = _swig_property(_webview.eWebView_microFocusChanged_get)
    selectionChanged = _swig_property(_webview.eWebView_selectionChanged_get)
    statusBarMessage = _swig_property(_webview.eWebView_statusBarMessage_get)
    statusBarVisibilityChangeRequested = _swig_property(_webview.eWebView_statusBarVisibilityChangeRequested_get)
    toolBarVisibilityChangeRequested = _swig_property(_webview.eWebView_toolBarVisibilityChangeRequested_get)
    unsupportedContent = _swig_property(_webview.eWebView_unsupportedContent_get)
    windowCloseRequested = _swig_property(_webview.eWebView_windowCloseRequested_get)
    javaScriptAlert = _swig_property(_webview.eWebView_javaScriptAlert_get)
    windowRequested = _swig_property(_webview.eWebView_windowRequested_get)
    authenticationRequired = _swig_property(_webview.eWebView_authenticationRequired_get)
    proxyAuthenticationRequired = _swig_property(_webview.eWebView_proxyAuthenticationRequired_get)
    sslErrors = _swig_property(_webview.eWebView_sslErrors_get)
eWebView.navigate = new_instancemethod(_webview.eWebView_navigate,None,eWebView)
eWebView.asciiInput = new_instancemethod(_webview.eWebView_asciiInput,None,eWebView)
eWebView.load = new_instancemethod(_webview.eWebView_load,None,eWebView)
eWebView.scroll = new_instancemethod(_webview.eWebView_scroll,None,eWebView)
eWebView.getHtml = new_instancemethod(_webview.eWebView_getHtml,None,eWebView)
eWebView.setHtml = new_instancemethod(_webview.eWebView_setHtml,None,eWebView)
eWebView.setZoomFactor = new_instancemethod(_webview.eWebView_setZoomFactor,None,eWebView)
eWebView.getZoomFactor = new_instancemethod(_webview.eWebView_getZoomFactor,None,eWebView)
eWebView.setDict = new_instancemethod(_webview.eWebView_setDict,None,eWebView)
eWebView.enablePersistentStorage = new_instancemethod(_webview.eWebView_enablePersistentStorage,None,eWebView)
eWebView.getRawCookies = new_instancemethod(_webview.eWebView_getRawCookies,None,eWebView)
eWebView.setRawCookies = new_instancemethod(_webview.eWebView_setRawCookies,None,eWebView)
eWebView_swigregister = _webview.eWebView_swigregister
eWebView_swigregister(eWebView)



