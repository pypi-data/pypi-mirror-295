import numpy as np
import time
from .SignalManager import SignalManager
from .Preprocessing import preprocess
import threading

def transpose(batch:np.ndarray):
	return batch.transpose([0,2,1])

ch_list = [0,1,2,3,4,5,6,7,8,9,10,11,12]
fs = 500
class BinaryBciSignalProcessing:
	def Construct(self):
		parameters = [
			
		]
		states = [
			"predictClass  3 0 0 0",
			"predictCount  8 0 0 0"
		]
		return (parameters, states)
		
	def Preflight(self, sigprops):
		pass
	
	def Initialize(self, indim, outdim): #indim[0] = ch
		self.ch = indim[0]
		self.is_run = False
	
	def StartRun(self):
		self.is_run = True
		self.signals = SignalManager(self.settings,self.ch)
		self.predict_class = 0
		self.predict_count = 0
		thread = threading.Thread(target=processing,args=[self])
		thread.start()

	def Process(self, stream_sig):
		trial_num = self.states['trialNum']
		true_class = self.states['trueClass'] # 0(wait) or 1 or 2 
		self.signals.add_signal(trial_num,stream_sig,true_class,self.predict_count,self.predict_class)
		self.states['predictClass'] = self.predict_class
		self.states['predictCount'] = self.predict_count
		
	
	def StopRun(self):
		self.is_run = False
		self.signals.reset_and_save()
		self.predict_count = 0
		
def processing(module:BinaryBciSignalProcessing):
	true_class = 0
	isall_reset = True
	module.predict_count = 0
	while module.is_run:
		true_class = module.states['trueClass']
		data = module.signals.get_last_samples()
		if data is None or true_class == 0:
			if (not isall_reset) and  true_class == 0:
				module.signals.reset_and_save()
				isall_reset = True
			module.predict_count = 0
			module.predict_class = 0
			time.sleep(0.01)
			continue
		isall_reset = False
		sig = np.asarray(data).astype('float32')
		sig = preprocess(sig[ch_list,:],fs)
		sig = transpose(np.array([sig]))
		fb = module.states["feedback"] # fb is 0 == true_class is 0
		#feedback
		prediction = module.loaded.predict(sig)[0]
		prediction = 1 if prediction > 0.5 else 0
		module.predict_class = prediction + 1 #round(np.mean(predict_list[-10:])) + 1
		module.predict_count += 1
		time.sleep(0.5)