# coding:utf8
	
from push_notifications.models import APNSDevice, GCMDevice

class Push(object):
	@staticmethod
	def Register(regid, uuid, name, platform):
		existingDevice = None
		if platform == 'android':
			existingDevice = GCMDevice.objects.filter(registration_id=regid)
		else:
			existingDevice = APNSDevice.objects.filter(registration_id=regid)
		if len(existingDevice) > 0:
			return False

		newDevice = None
		if platform == 'android':
			newDevice = GCMDevice()
		else:
			newDevice = APNSDevice()

		try:
			newDevice.registration_id = regid
			newDevice.device_id = uuid
			newDevice.name = name
			newDevice.save()
			return True
		except Exception, e:
			print e
			return False

	@staticmethod
	def Send(message, payload):
		android_devices = GCMDevice.objects.all()
		ios_devices = APNSDevice.objects.all()
		try:
			android_devices.send_message(message, extra=payload)
		except Exception, e:
			print e

		try:
			ios_devices.send_message(message, extra=payload)
		except Exception, e:
			print e