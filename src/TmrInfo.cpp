/*
 * TmrInfo.cpp
 *
 *     Author: Measurement Computing Corporation
 */

#include "TmrInfo.h"

namespace ul
{

TmrInfo::TmrInfo()
{
	mNumTimers = 0;
	mMinFreq = 0;
	mMaxFreq = 0;
	mType = (TimerType) 0;
	mScanOptions = SO_DEFAULTIO;
	mTriggerTypes = TRIG_NONE;
}

TmrInfo::~TmrInfo()
{

}

void TmrInfo::setNumTimers(int numTimers)
{
	mNumTimers = numTimers;
}

int TmrInfo::getNumTimers() const
{
	return mNumTimers;
}

void TmrInfo::setTimerType(TimerType type)
{
	mType = type;
}

TimerType TmrInfo::getTimerType(int tmrNum) const
{
	TimerType type = (TimerType) 0;

	if(tmrNum < mNumTimers)
		type = mType;

	return type;
}

void TmrInfo::setMinFrequency(double minFreq)
{
	mMinFreq = minFreq;
}

double TmrInfo::getMinFrequency() const
{
	return mMinFreq;
}

void TmrInfo::setMaxFrequency(double maxFreq)
{
	mMaxFreq = maxFreq;
}

double TmrInfo::getMaxFrequency() const
{
	return mMaxFreq;
}

void TmrInfo::setScanOptions(long long options)
{
	mScanOptions = (ScanOption) options;
}

ScanOption TmrInfo::getScanOptions() const
{
	return mScanOptions;
}
/*
void TmrInfo::addTriggerType(TriggerType triggerType)
{
	mTriggerTypes.push_back(triggerType);
}


std::vector<TriggerType> TmrInfo::getTriggerTypes() const
{
	return mTriggerTypes;
}

void TmrInfo::getTriggerTypes(TriggerType types[], int* count) const
{
	if(mTriggerTypes.size() <= (unsigned int)*count )
		std::copy(mTriggerTypes.begin(), mTriggerTypes.end(), types);

	*count = mTriggerTypes.size();
}

int TmrInfo::getTriggerTypeCount() const
{
	return mTriggerTypes.size();
}

TriggerType TmrInfo::getTriggerType(unsigned int index) const
{
	TriggerType type = (TriggerType) 0;

	if(index < mTriggerTypes.size())
		type = mTriggerTypes[index];

	return type;
}*/

void TmrInfo::setTriggerTypes(long long triggerTypes)
{
	mTriggerTypes = (TriggerType) triggerTypes;
}


TriggerType TmrInfo::getTriggerTypes() const
{
	return mTriggerTypes;
}

bool TmrInfo::supportsTrigger() const
{
	bool supportsTrig = false;

	if(mTriggerTypes)
		supportsTrig = true;

	return supportsTrig;
}

} /* namespace ul */
