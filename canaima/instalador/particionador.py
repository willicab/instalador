import parted

def add_partition():
    myDev = parted.Device(path="/dev/sdc")
    myDisk = parted.freshDisk(myDev, 'msdos')
    myConstraint = parted.Constraint(device = myDev)
    print myDev.sectorSize
    cien = (512 * myDev.sectorSize)
    # Fill the entire Disk with a single partition
    myGeometry = parted.Geometry(device=myDev, start=1, end=(cien * 8)) 
    #myGeometry = parted.Geometry(device=myDev, start=1, end=(myConstraint.maxSize / 2))
    myFileSystem = parted.FileSystem(type="ext3", geometry=myGeometry)
    # Create the partition object using the objects we defined before
    myPartition = parted.Partition(disk=myDisk, fs=myFileSystem,
        type=parted.PARTITION_NORMAL, geometry=myGeometry)
    # Redefine myConstraint to snap to the exact limits
    myConstraint = parted.Constraint(exactGeom = myGeometry)
 
    # Add partition to the disk. Will return True if successful
    myDisk.addPartition(partition = myPartition, constraint=myConstraint)
    # Write changes to the disk. Up until this point, no changes have been made to the disk. everything is sitting in memmory
    myDisk.commit()
    print myPartition.path
    
add_partition()
