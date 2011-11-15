#!/usr/bin/python
# coding: utf-8

import subprocess
import parted
import re
import os

TARGET_DEVICE = "/dev/sda4"

class Block:
	def __init__(self, name, parent):
		block_path = "/sys/block/" + parent 
		if parent!=name:
			block_path = block_path + "/" + name
		self.parent = parent
		self.name = name
		nums = re.split("[:\n]",file(block_path + "/dev").readlines()[0])
		self.major = nums[0]
		self.minor = nums[1]

		self.attributes = {}
		self.attributes["name"] = name
		for att_name in ["vendor", "model", "serial"]:
			try:
				f = file("/sys/block/" + parent + "/device/" + att_name, "r")
				self.attributes[att_name] = re.split("[\n ]+", f.read())[0]
			except IOError:
				self.attributes[att_name] = None

		if name.find("hd")==0: self.attributes["bus"] = "ide"
		else: self.attributes["bus"] = "scsi"
		
		majorminor = "%x,%x" % (int(self.major),int(self.minor))
		if os.popen("stat -c %t,%T /dev/" + self.name + " 2> /dev/null").readline() == majorminor:
			self.dev = "/dev/" + self.name
		else:
			for file_name in os.popen("find /dev -type b -regex \"[^\.]*\"").readlines():
				ps = os.popen("stat -c %t,%T " + file_name)
				stat = ps.readline()
				ps.close()
				if stat.find(majorminor)==0:
					self.dev = file_name[:len(file_name)-1]
					return
					
def get_partitions():
  """
  Find the partitions in the system
  """

  blocks = {}
  partitions = []
  partitions_file = open('/proc/partitions', "r")
  lines = partitions_file.readlines()
  for line in lines[2:]:
    partition = re.split('\s+', line)[4]
    device = re.compile("([a-z]+)([0-9]+)?").match(partition).groups()[0]

    if partition == device:
      block_path = "/sys/block/" + device
    else:
      block_path = "/sys/block/" + device + "/" + partition

    try:
      os.stat(block_path)
      #os.stat("/dev/" + partition)
      partitions.append(partition)
      block = Block(partition, device)
      blocks[block.name] = block
      blocks[block.dev] = block
    except OSError:
      pass
    except AttributeError:
      print "Not suitable dev for " + block.name
  #print blocks
  return partitions
        
p = subprocess.Popen("dumpe2fs -h %s" % TARGET_DEVICE,
                     shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

lines = p.stdout.readlines()

free_blocks = 0
block_size = 0
for l in lines:
    if l.startswith("Free blocks:"):
        free_blocks = int(l.split()[2])
    elif l.startswith("Block size:"):
        block_size = int(l.split()[2])


device = parted.Device("/dev/sdb")
disk = parted.Disk(device)
partition = None
#print get_partitions()
#print 'Path', 'bytes', 'Kb', 'Mb', 'Gb', 'start', 'end'
print 'device.sectorSize: ' + str(device.sectorSize)
print '------------------------------------------------------------------------'

for p in disk.partitions:
    #print p.path
    #if p.path == TARGET_DEVICE:
    partition = p
    sectors_unused = free_blocks * (block_size/float(device.sectorSize))
    sectors_unused = (partition.geometry.end - partition.geometry.start + 1) - sectors_unused
    bytes = sectors_unused * 512
    kb = bytes / 1024
    mb = kb / 1024
    gb = mb / 1024
    print 'Path:  ' + str(p.path)
    print 'Bytes: ' + str(bytes)
    print 'Kb:    ' + str(kb)
    print 'Mb:    ' + str(mb)
    print 'Gb:    ' + str(gb)
    print 'Start: ' + str(partition.geometry.start)
    print 'End:   ' + str(partition.geometry.end)
    print '--------------------------------------------------------------------'
