/*
 * UlAiConfig.h
 *
 *     Author: Measurement Computing Corporation
 */

#ifndef INTERFACES_ULAICONFIG_H_
#define INTERFACES_ULAICONFIG_H_

#include "../uldaq.h"

namespace ul
{

class UlAiConfig
{
public:
	virtual ~UlAiConfig() {};

	virtual void setChanType(int channel, AiChanType chanType) = 0;
	virtual AiChanType getChanType(int channel) = 0;

	virtual void setChanTcType(int channel, TcType tcType) = 0;
	virtual TcType getChanTcType(int channel) = 0;

	virtual void setChanTempUnit(int channel, TempUnit unit) = 0;
	virtual TempUnit getChanTempUnit(int channel) = 0;
	virtual void setTempUnit(TempUnit unit) = 0;

	virtual void setAutoZeroMode(AutoZeroMode mode) = 0;
	virtual AutoZeroMode getAutoZeroMode() = 0;

	virtual void setAdcTimingMode(AdcTimingMode mode) = 0;
	virtual AdcTimingMode getAdcTimingMode() = 0;

	virtual void setChanIepeMode(int channel, IepeMode mode) = 0;
	virtual IepeMode getChanIepeMode(int channel) = 0;

	virtual void setChanCouplingMode(int channel, CouplingMode mode) = 0;
	virtual CouplingMode getChanCouplingMode(int channel) = 0;

	virtual void setChanSensorSensitivity(int channel, double sensitivity) = 0;
	virtual double getChanSensorSensitivity(int channel) = 0;

	virtual void setChanSlope(int channel, double slope) = 0;
	virtual double getChanSlope(int channel) = 0;

	virtual void setChanOffset(int channel, double offset) = 0;
	virtual double getChanOffset(int channel) = 0;

	virtual unsigned long long getCalDate() = 0; // returns number of seconds since unix epoch
	virtual void getCalDateStr(char* calDate, unsigned int* maxStrLen) = 0;
};

} /* namespace ul */

#endif /* INTERFACES_ULAICONFIG_H_ */
