import json
import uuid
import os.path
from copy import deepcopy

config = json.load(open(os.path.join("..", "www", "config.json")))

lpri = len(config["priorities"])-1

def _calcpriority(priority, time):
	for i in config["priority_thresh"]:
		if time >= i:
			priority -= 1
	return max(priority, 0)

def _concatlist(lists):
	masterlist = []
	for i in lists: 
		for j in i:
			masterlist.append(j)
	return masterlist

class Queue:
	def __init__(self):
		self.queue = [[] for i in config["priorities"]]
	def append(self, name, priority, esttime, material):
		esttime = min(360, max(0.1, esttime))

		priority = _calcpriority(priority, esttime)

		inqueue = False
		for i in self.queue:
			for j in i: 
				if name.lower() == j["name"].lower() and material == j["material"]:
					inqueue = True
					break

		if not inqueue:
			self.queue[lpri-priority].append({
				"priority": lpri-priority,
				"name": name.title().strip().rstrip(),
				"material": material,
				"esttime": esttime,
				"coachmodified": False,
				"uuid": str(uuid.uuid1())
			})

	def passoff(self, priority, index=0):
		if not priority and len(self.queue[lpri-priority]) < index:
			return
		item = self.queue[lpri-priority].pop(index)
		index += 1
		if len(self.queue[lpri-priority]) < index:
			priority -= 1
			index = 0
		item["priority"] = lpri-priority
		self.queue[lpri-priority].insert(max(index, 0),item)
		
	def move(self, in1, in2, pr1, pr2):
		item = self.queue[lpri-pr1].pop(in1)
		item["coachmodified"] = True
		item["priority"] = lpri-priority
		if in2 >= 0:
			self.queue[lpri-pr2].insert(in2, item)
		else:
			self.queue[lpri-pr2].append(item)
	def remove(self, priority, index):

		del self.queue[lpri-priority][index]
	def sremove(self, index):
		masterqueue = _concatlist(self.queue)
		target = masterqueue[index] 
		for i in self.queue:
			if target in i:
				i.remove(target)
	def spass(self, oindex):
		masterqueue = _concatlist(self.queue)
		if oindex == len(masterqueue)-1: return
		target = masterqueue[oindex]
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if target in i:
				i.remove(target)
		end = masterqueue[oindex+1]
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if end in i:
				tindex = i.index(end)
				tpri = lpri-ii
		target["priority"] = lpri-tpri
		self.queue[lpri-tpri].insert(tindex+1, target)

	def smove(self, oi, ni, np):
		masterqueue = _concatlist(self.queue)
		target = masterqueue[oi]
		for i in self.queue:
			if target in i:
				i.remove(target)
		target["coachmodified"] = True
		target["priority"] = lpri-np
		self.queue[lpri-np].insert(ni, target)

	def sincrement(self, index):
		masterqueue = _concatlist(self.queue)
		target = masterqueue[index] 
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if target in i:
				index = i.index(target)
				priority = lpri-ii

		if priority == lpri and not index:
			return
		item = self.queue[lpri-priority].pop(index)
		index -= 1
		if index < 0:
			priority += 1
			if priority > lpri:
				index = 0
				priority = lpri
			else:
				index = len(self.queue[max(lpri-priority, 0)])
		item["coachmodified"] = True
		item["priority"] = lpri-priority
		self.queue[max(lpri-priority, 0)].insert(min(index, len(self.queue[max(lpri-priority, 0)])),item)

	def sdecrement(self, index):
		masterqueue = _concatlist(self.queue)
		target = masterqueue[index] 
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if target in i:
				index = i.index(target)
				priority = lpri-ii

		if not priority and len(self.queue[lpri-priority]) < index:
			return
		item = self.queue[lpri-priority].pop(index)
		index += 1
		if len(self.queue[lpri-priority]) < index:
			priority -= 1
			if priority < 0:
				index = len(self.queue[min(lpri-priority, lpri)])
				priority = 0
			else:
				index = 0
		item["coachmodified"] = True
		item["priority"] = lpri-priority
		self.queue[min(lpri-priority, lpri)].insert(max(index, 0),item)
	
	# uuid update




	def uremove(self, u):
		for i in self.queue:
			for j in i:
				if j["uuid"] == u:
					i.remove(j)
	def upass(self, u):
		masterqueue = _concatlist(self.queue)
		for i in self.queue:
			for j in i:
				if j["uuid"] == u:
					oindex = masterqueue.index(j)

		if oindex == len(masterqueue)-1: return
		target = masterqueue[oindex]
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if target in i:
				i.remove(target)
		end = masterqueue[oindex+1]
		for ii in range(len(self.queue)):
			i = self.queue[ii]
			if end in i:
				tindex = i.index(end)
				tpri = lpri-ii
		target["priority"] = lpri-tpri
		self.queue[lpri-tpri].insert(tindex+1, target)

	def umove(self, u, ni, np):
		for i in self.queue:
			for j in i:
				if j["uuid"] == u:
					target = deepcopy(j)
					i.remove(j)
		target["coachmodified"] = True
		target["priority"] = lpri-np
		self.queue[lpri-np].insert(ni, target)

	def uincrement(self, u):
		for i in self.queue:
			for j in i:
				if j["uuid"] == u:
					index = j.index(i)
					priority = self.queue.index(i)

		if priority == lpri and not index:
			return
		item = self.queue[lpri-priority].pop(index)
		index -= 1
		if index < 0:
			priority += 1
			if priority > lpri:
				index = 0
				priority = lpri
			else:
				index = len(self.queue[max(lpri-priority, 0)])
		item["coachmodified"] = True
		item["priority"] = lpri-priority
		self.queue[max(lpri-priority, 0)].insert(min(index, len(self.queue[max(lpri-priority, 0)])),item)

	def udecrement(self, u):
		for i in self.queue:
			for j in i:
				if j["uuid"] == u:
					index = j.index(i)
					priority = self.queue.index(i)

		if not priority and len(self.queue[lpri-priority]) < index:
			return
		item = self.queue[lpri-priority].pop(index)
		index += 1
		if len(self.queue[lpri-priority]) < index:
			priority -= 1
			if priority < 0:
				index = len(self.queue[min(lpri-priority, lpri)])
				priority = 0
			else:
				index = 0
		item["coachmodified"] = True
		item["priority"] = lpri-priority
		self.queue[min(lpri-priority, lpri)].insert(max(index, 0),item)
