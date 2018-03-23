/*
 * AiDevice.h
 *
 *     Author: Measurement Computing Corporation
 */

#ifndef AIDEVICE_H_
#define AIDEVICE_H_

#include "ul_internal.h"
#include "IoDevice.h"
#include "AiInfo.h"
#include "AiConfig.h"
#include <vector>

namespace ul
{
class UL_LOCAL AiDevice: public IoDevice, public UlAiDevice
{
public:
	virtual ~AiDevice();
	AiDevice(const DaqDevice& daqDevice);

	virtual const UlAiInfo& getAiInfo() { return mAiInfo;}
	virtual UlAiConfig& getAiConfig() { return *mAiConfig;}

	virtual double aIn(int channel, AiInputMode inputMode, Range range, AInFlag flags);
	virtual double aInScan(int lowChan, int highChan, AiInputMode inputMode, Range range, int samplesPerChan, double rate, ScanOption options, AInScanFlag flags, double data[]);
	virtual void aInLoadQueue(AiQueueElement queue[], unsigned int numElements);
	virtual void setTrigger(TriggerType type, int trigChan, double level, double variance, unsigned int retriggerCount);

	virtual UlError getStatus(ScanStatus* status, TransferStatus* xferStatus);
	virtual void stopBackground();

	double convertTempUnit(double tempC, TempUnit unit);

	//////////////////////          Configuration functions          /////////////////////////////////
	virtual void setCfg_ChanType(int channel, AiChanType chanType);
	virtual AiChanType getCfg_ChanType(int channel) const;

	virtual void setCfg_ChanTcType(int channel, TcType tcType);
	virtual TcType getCfg_ChanTcType(int channel) const;

	virtual void setCfg_TempUnit(TempUnit unit);
	//virtual TempUnit getCfg_TempUnit() const;

	virtual void setCfg_ChanTempUnit(int channel, TempUnit unit);
	virtual TempUnit getCfg_ChanTempUnit(int channel) const;

	virtual void setCfg_AutoZeroMode(AutoZeroMode mode);
	virtual AutoZeroMode getCfg_AutoZeroMode() const;

	virtual void setCfg_AdcTimingMode(AdcTimingMode mode);
	virtual AdcTimingMode getCfg_AdcTimingMode();

	virtual void setCfg_ChanIepeMode(int channel, IepeMode mdoe);
	virtual IepeMode getCfg_ChanIepeMode(int channel);

	virtual void setCfg_ChanCouplingMode(int channel, CouplingMode mode);
	virtual CouplingMode getCfg_ChanCouplingMode(int channel);

	virtual void setCfg_ChanSensorSensitivity(int channel, double sensitivity);
	virtual double getCfg_ChanSensorSensitivity(int channel);

	virtual void setCfg_ChanSlope(int channel, double slope);
	virtual double getCfg_ChanSlope(int channel);
	virtual void setCfg_ChanOffset(int channel, double offset);
	virtual double getCfg_ChanOffset(int channel);

	virtual unsigned long long getCfg_CalDate();
	virtual void getCfg_CalDateStr(char* calDate, unsigned int* maxStrLen);

protected:
	virtual void loadAdcCoefficients() = 0;
	virtual int getCalCoefIndex(int channel, AiInputMode inputMode, Range range) const = 0;
	virtual double calibrateData(int channel, AiInputMode inputMode, Range range, unsigned int count, long long flags) const;

	virtual CalCoef getCalCoef(int channel, AiInputMode inputMode, Range range, long long flags) const;
	std::vector<CalCoef> getScanCalCoefs(int lowChan, int highChan, AiInputMode inputMode, Range range, long long flags) const;
	bool queueEnabled() const;
	int queueLength() const;

	void check_AIn_Args(int channel, AiInputMode inputMode, Range range, AInFlag flags) const;
	void check_AInScan_Args(int lowChan, int highChan, AiInputMode inputMode, Range range, int samplesPerChan, double rate, ScanOption options, AInScanFlag flags, double data[]) const;
	void check_AInLoadQueue_Args(const AiQueueElement queue[], unsigned int numElements) const;
	void check_AInSetTrigger_Args(TriggerType trigtype, int trigChan,  double level, double variance, unsigned int retriggerCount) const;

	bool isValidChanQueue(const AiQueueElement queue[], unsigned int numElements) const;
	bool isValidGainQueue(const AiQueueElement queue[], unsigned int numElements) const;
	bool isValidModeQueue(const AiQueueElement queue[], unsigned int numElements) const;

	void initCustomScales();
	std::vector<CustomScale> getCustomScales(int lowChan, int highChan) const;

	void enableCalMode(bool enable) { mCalModeEnabled = enable;}
	bool calModeEnabled() const { return mCalModeEnabled;}

	virtual void readCalDate() {};

protected:
	AiInfo mAiInfo;
	AiConfig* mAiConfig;
	std::vector<CalCoef> mCalCoefs;
	std::vector<CustomScale> mCustomScales;
	std::vector<AiQueueElement> mAQueue;

	std::vector<TempUnit> mChanTempUnit;

	unsigned long long mCalDate; // cal date in sec

private:
	bool mCalModeEnabled;

};

} /* namespace ul */

#endif /* AIDEVICE_H_ */
