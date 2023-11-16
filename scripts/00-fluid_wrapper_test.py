import fluid_wrapper

src = "/Volumes/Public/Archives/Disques durs SCSI Akai/HD 2/Carmaux 2015 PADSsos/1 B-2 PICK 3.wav"

mfcc = fluid_wrapper.mfcc(src)
stats = fluid_wrapper.stats(mfcc)

print(fluid_wrapper._wave_to_np(stats))

fluid_wrapper._remove_temp()