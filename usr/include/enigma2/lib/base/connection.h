#ifndef __connection_h
#define __connection_h

#include <lib/base/sigc.h>
#include <lib/base/object.h>

class eConnection: public iObject, public sigc::connection
{
	DECLARE_REF(eConnection);
	ePtr<iObject> m_owner;
public:
	eConnection(iObject *owner, const sigc::connection &conn);
	virtual ~eConnection();
};

#endif
