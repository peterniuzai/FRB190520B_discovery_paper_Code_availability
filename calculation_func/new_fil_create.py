import numpy as np
from sigpyproc.Readers import FilReader

def new_filterbank_create(sample_ID,filename,filterbank_new_dir,sample_delay,rank_pulse):
	'''
	Specific for creating the new filterbank files based on the old one
	Connect the last or next files.

	'''
        rank_pulse = rank_pulse
        filename_next = filename[:-4]+'_next.fil'
        filename_last = filename[:-4]+'_last.fil'
        f_read = FilReader(filename)
        f_read.header.tstart = f_read.header.tstart+(sample_ID-20000)*f_read.header.tsamp/3600./24
        f_new = f_read.header.prepOutfile(filterbank_new_dir+'FRB190520_cand_%04d.fil'%(rank_pulse),nbits=32)
        if sample_ID + sample_delay < f_read.header['nsamples'] and sample_ID - 20000 > 0:
                        data = f_read.readBlock(sample_ID-20000,20000 + sample_delay)
                        f_new.write(data)
        elif sample_ID + sample_delay > f_read.header['nsamples'] and sample_ID -20000 > 0 : #and os.path.exists(filename_next):
                        print 'Take next filterbank....'
                        f_next   = FilReader(filename_next)
                        data_stack = f_next.readBlock(0,sample_delay-(f_read.header.nsamples-sample_ID))
                        data = f_read.readBlock(sample_ID-20000,f_read.header['nsamples']-sample_ID+20000)
                        f_new.write(data)
                        f_new.write(data_stack)
        elif sample_ID -20000 < 0: # and os.path.exists(filename_last):
                        print 'Take last filterbank....'
                        data = f_read.readBlock(0,sample_delay+sample_ID)
                        f_last = FilReader(filename_last)
                        data_stack = f_last.readBlock(f_read.header.nsamples-(20000-sample_ID),20000-sample_ID)

                        f_new.write(data_stack)
                        f_new.write(data)

        f_new.close()
