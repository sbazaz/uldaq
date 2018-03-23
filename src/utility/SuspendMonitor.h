/*
 * SuspendMonitor.h
 *
 *  Created on: Jan 2, 2018
 *     Author: Measurement Computing Corporation
 */

#ifndef UTILITY_SUSPENDMONITOR_H_
#define UTILITY_SUSPENDMONITOR_H_

#include "../ul_internal.h"
#include "ThreadEvent.h"

namespace ul
{

class SuspendMonitor
{
public:

	static SuspendMonitor& instance()
	{
		static SuspendMonitor mInstance;
		return mInstance;
	}

	void start();
	void terminate();
	inline unsigned long long getCurrentSystemSuspendCount() { return mSystemSuspendCount;}

protected:
	SuspendMonitor();

private:
	static void* suspendDetectionThread(void *arg);

private:
	pthread_t mSuspendDetectionThread;
	bool mTerminateSuspendDetectionThread;
	unsigned long long mSystemTimeRecorded;
	unsigned long long mSystemSuspendCount;

	ThreadEvent mEvent;

};

} /* namespace ul */

#endif /* UTILITY_SUSPENDMONITOR_H_ */
