#!/usr/bin/env python
"""driver.py -- creates scripts for batch-submission of cmsRun jobs
"""
from __future__ import print_function
import argparse
import os
import sys
import math
import datetime

from JMETriggerAnalysis.NTuplizers.utils.common import *

def batch_job_HTCondor(**kwargs):

    _OUTPUT_DIR = os.path.abspath(os.path.realpath(kwargs['output_directory']))

    EXE('mkdir -p '+_OUTPUT_DIR+'/'+kwargs['output_subdirectory'], verbose=kwargs['verbose'], dry_run=kwargs['dry_run'])

    _OFILE_ABSPATH = _OUTPUT_DIR+'/'+kwargs['output_basename']+'.sh'

    if os.path.exists(_OFILE_ABSPATH):
       KILL(log_prx+' -- batch_job_HTCondor: target output file already exists: '+_OFILE_ABSPATH)

    # batch configuration options
    _OPTS = [

      'batch_name = '+kwargs['output_basename'],

      'executable = '+_OFILE_ABSPATH,

      'output = '+_OUTPUT_DIR+'/'+kwargs['output_subdirectory']+'/'+kwargs['output_basename']+'.out.$(Cluster).$(Process)',
      'error  = '+_OUTPUT_DIR+'/'+kwargs['output_subdirectory']+'/'+kwargs['output_basename']+'.err.$(Cluster).$(Process)',
      'log    = '+_OUTPUT_DIR+'/'+kwargs['output_subdirectory']+'/'+kwargs['output_basename']+'.log.$(Cluster).$(Process)',

      '#arguments = ',

      'transfer_executable = True',

      'universe = vanilla',

      'getenv = True',

      'should_transfer_files = IF_NEEDED',
      'when_to_transfer_output = ON_EXIT',

      'requirements = (OpSysAndVer == "'+('CentOS7' if kwargs.get('is_slc7_arch', True) else 'SL6')+'")',

      'RequestCpus = '+str(kwargs.get('RequestCpus', 1)),

      ' RequestMemory  = '+str(kwargs.get('RequestMemory', 2000)),
      '+RequestRuntime = '+str(kwargs.get('+RequestRuntime', 10800)),
    ]

    if 'transfer_input_files' in kwargs:
       _OPTS += ['transfer_input_files    = '+(','.join(kwargs['transfer_input_files']))]

    _OPTS += ['queue']

    _UPDATED_OPTS = []

    _ADDED_OPTS = (kwargs['submit_options'] if 'submit_options' in kwargs else [])

    for _tmp_opt in _OPTS[:-1]:

        _tmp_opt_keyw = _tmp_opt.split('=')[0].replace(' ','')

        _tmp_skip_opt = False

        for _tmp_add_opt in _ADDED_OPTS:

            _tmp_add_opt_keyw = _tmp_add_opt.split('=')[0].replace(' ','')

            if _tmp_opt_keyw == _tmp_add_opt_keyw: _tmp_skip_opt = True; break;

        if _tmp_skip_opt: continue

        _UPDATED_OPTS += [_tmp_opt]

    for _tmp_add_opt in _ADDED_OPTS: _UPDATED_OPTS += [_tmp_add_opt]

    if 'queue' not in _UPDATED_OPTS[-1]: _UPDATED_OPTS += ['queue']

    _o_file = open(_OFILE_ABSPATH, 'w')

    _o_shebang = '#!/bin/bash'
    _o_file.write(_o_shebang+'\n')

    # export explicitly the environment variable LD_LIBRARY_PATH
    if kwargs.get('export_LD_LIBRARY_PATH', False):
       if 'LD_LIBRARY_PATH' in os.environ:
          _o_file.write('\n'+'export LD_LIBRARY_PATH='+os.environ['LD_LIBRARY_PATH']+'\n')

    _o_file.write('\n'+kwargs['output_string']+'\n')

    _o_file.close()

    print('\033[1m'+'\033[94m'+'output:'+'\033[0m', os.path.relpath(_OFILE_ABSPATH, os.environ['PWD']))

    EXE('chmod u+x '+_OFILE_ABSPATH, verbose=kwargs['verbose'], dry_run=kwargs['dry_run'])

    _OFCFG_ABSPATH = os.path.splitext(_OFILE_ABSPATH)[0]+'.htc'

    _o_fcfg = open(_OFCFG_ABSPATH, 'w')

    for _tmp in _UPDATED_OPTS: _o_fcfg.write(_tmp+'\n')

    _o_fcfg.close()

    if kwargs['submit']:
       EXE('condor_submit '+_OFCFG_ABSPATH, suspend=False, verbose=kwargs['verbose'], dry_run=kwargs['dry_run'])

    return

def convert_args_to_lines(args):

    _tmp_lines = []

    _tmp_idxs = [0] + [i_idx for i_idx, i_opt in enumerate(args) if i_opt.startswith('-') and not (is_int(i_opt) or is_float(i_opt))] + [len(args)]
    _tmp_idxs = sorted(list(set(_tmp_idxs)))

    for j_idx in range(len(_tmp_idxs)-1):
        _tmp_lines += [' '.join(args[_tmp_idxs[j_idx]:_tmp_idxs[j_idx+1]])]

    del _tmp_idxs

    return _tmp_lines

#### main
if __name__ == '__main__':
    ### args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', '--cfg', dest='cmsRun_cfg', action='store', default=None, required=True,
                        help='path to cmsRun cfg file')

    parser.add_argument('--customize-cfg', dest='customize_cfg', action='store_true', default=False,
                        help='append minimal customization to cmsRun-cfg required by the driver')

    parser.add_argument('-d', '--dataset', dest='dataset', action='store', default=None, required=True,
                        help='name of MINIAOD* input data set in DAS')

    parser.add_argument('-o', '--output', dest='output', action='store', default=None, required=True,
                        help='path to output directory')

    parser.add_argument('--name', dest='name', action='store', default='job', required=False,
                        help='prefix of output files\' names (example: [NAME]_[counter].[ext])')

    parser.add_argument('-f', '--max-files', dest='max_files', action='store', type=int, default=-1, required=False,
                        help='maximum number of input files to be processed (if integer is negative, all files will be processed)')

    parser.add_argument('-m', '--max-events', dest='max_events', action='store', type=int, default=-1, required=False,
                        help='maximum number of total input events to be processed (if integer is negative, all events will be processed)')

    parser.add_argument('-n', '--n-events', dest='n_events', action='store', type=int, default=-1, required=False,
                        help='maximum number of events per job')

    parser.add_argument('--cpus', dest='cpus', action='store', type=int, default=1, required=False,
                        help='argument of HTC parameter "RequestCpus"')

    parser.add_argument('--memory', dest='memory', action='store', type=int, default=2000, required=False,
                        help='argument of HTC parameter "RequestMemory"')

    parser.add_argument('--runtime', dest='runtime', action='store', type=int, default=10800, required=False,
                        help='argument of HTC parameter "+RequestRuntime"')

    parser.add_argument('--batch', dest='batch', choices=['htc'], action='store', default='htc',
                        help='type of batch system for job submission')

    parser.add_argument('--htc-opts', dest='htc_opts', nargs='+', default=[],
                        help='list of options for HTCondor submission script')

    parser.add_argument('--submit', dest='submit', action='store_true', default=False,
                        help='submit job(s) on the batch system')

    parser.add_argument('--no-export-LD-LIBRARY-PATH', dest='no_export_LD_LIBRARY_PATH', action='store_true', default=False,
                        help='do not export explicitly the environment variable "LD_LIBRARY_PATH" in the batch-job executable')

    parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False,
                        help='enable dry-run mode')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help='enable verbose mode')

    opts, opts_unknown = parser.parse_known_args()
    ### -------------------------

    log_prx = os.path.basename(__file__)+' -- '

    ### opts --------------------
    VERBOSE = bool(opts.verbose and (not opts.submit))

    if not os.path.isfile(opts.cmsRun_cfg):
       KILL(log_prx+'invalid path to cmsRun cfg file [-c]: '+str(opts.cmsRun_cfg))

    if os.path.exists(opts.output):
       KILL(log_prx+'target path to output directory already exists [-o]: '+str(opts.output))

    OUTPUT_DIR = os.path.abspath(opts.output)

    if opts.n_events == 0:
       KILL(log_prx+'logic error: requesting zero events per job (use non-zero value for argument of option "-n")')

    if opts.batch != None:
       if opts.submit and (not opts.dry_run):
          if opts.batch == 'htc': which('condor_submit')

    if opts.cpus <= 0:
       KILL(log_prx+'invalid (non-positive) value for HTC parameter "RequestCpus": '+str(opts.cpus))

    if opts.memory <= 0:
       KILL(log_prx+'invalid (non-positive) value for HTC parameter "RequestMemory": '+str(opts.memory))

    if opts.runtime <= 0:
       KILL(log_prx+'invalid (non-positive) value for HTC parameter "+RequestRuntime": '+str(opts.runtime))

    is_slc7_arch = False
    if os.environ['SCRAM_ARCH'].startswith('slc7'): is_slc7_arch = True
    elif os.environ['SCRAM_ARCH'].startswith('slc6'): pass
    else:
       KILL(log_prc+'could not infer architecture from environment variable "SCRAM_ARCH": '+str(os.environ['SCRAM_ARCH']))

    ### unrecognized command-line arguments
    ### -> used as additional command-line arguments to cmsRun
    if len(opts_unknown):
       print('-'*50)
       print(colored_text('additional cmsRun command-line arguments:', ['1']))
       for _tmp in opts_unknown: print(' '+str(_tmp))
       print('-'*50)

    ### extract input-files information from data set name via dasgoclient
    ### -> list of dictionaries, each containing names of MINIAOD files, RAW parent files, and number of events per file
    dataset_split = opts.dataset.split('/')
    if len(dataset_split) != 4:
       KILL(log_prx+'invalid data-set name (format is incorrect, check slashes): '+opts.dataset)

    if 'MINIAOD' not in dataset_split[3]:
       KILL(log_prx+'the data set\'s Tier is not MINIAOD*: '+opts.dataset)

    dataset_files = command_output_lines('dasgoclient --query "file dataset='+str(opts.dataset)+'"')
    dataset_files = [_tmp for _tmp in dataset_files if _tmp != '']
    dataset_files = sorted(list(set(dataset_files)))

    if len(dataset_files) == 0:
       KILL(log_prx+'empty list of input files for dataset: '+str(opts.dataset))

    if opts.max_events == 0:
       KILL(log_prx+'logic error: requesting a maximum of zero input events (use non-zero value for argument of option --max-events/-m)')

    if opts.max_files == 0:
       KILL(log_prx+'logic error: requesting a maximum of zero input files (use non-zero value for argument of option --max-files/-f)')

    elif opts.max_files > 0:
       dataset_files = dataset_files[:opts.max_files]

    inputfileDicts = []
    tot_events, break_loop = 0, False

    for i_file in dataset_files:
        i_file_nevents = command_output_lines('dasgoclient --query "file='+str(i_file)+' | grep file.nevents"')
        i_file_nevents = [_tmp.replace(' ', '') for _tmp in i_file_nevents]
        i_file_nevents = [_tmp for _tmp in i_file_nevents if _tmp != '']
        i_file_nevents = sorted(list(set(i_file_nevents)))

        if len(i_file_nevents) != 1:
           KILL('AAA')

        i_file_nevents = i_file_nevents[0]

        if not is_int(i_file_nevents):
           KILL('BBB')

        i_file_nevents = int(i_file_nevents)

        tot_events += i_file_nevents
        if (opts.max_events > 0) and (tot_events >= opts.max_events):
           i_file_nevents -= (tot_events - opts.max_events)
           break_loop = True

        if opts.verbose:
           print(i_file)
           print(i_file_nevents)

        i_file_rawparents = []

        i_file_aodfiles = command_output_lines('dasgoclient --query "parent file='+str(i_file)+'"')
        i_file_aodfiles = [_tmp for _tmp in i_file_aodfiles if _tmp != '']
        i_file_aodfiles = sorted(list(set(i_file_aodfiles)))
        for i_file_aodf in i_file_aodfiles:
            i_file_rawfiles_tmp = command_output_lines('dasgoclient --query "parent file='+str(i_file_aodf)+'"')
            i_file_rawfiles_tmp = [_tmp.replace(' ', '') for _tmp in i_file_rawfiles_tmp]
            i_file_rawfiles_tmp = [_tmp for _tmp in i_file_rawfiles_tmp if _tmp != '']
            i_file_rawfiles_tmp = sorted(list(set(i_file_rawfiles_tmp)))
            i_file_rawparents += i_file_rawfiles_tmp

        i_file_rawparents = sorted(list(set(i_file_rawparents)))

        if opts.verbose:
           for _tmp in i_file_rawparents:
               print(' '*5, _tmp)

        inputfileDicts += [{
          'filesMINIAOD': [i_file],
          'filesMINIAOD.nevents': i_file_nevents,
          'filesRAW': i_file_rawparents,
        }]

        if break_loop:
           break

    del tot_events, break_loop

    ### total number of events and jobs
    ### -> used to determine format of output-file name
    njobs = 0
    for i_inpfdc in inputfileDicts:
        njobs += int(math.ceil(float(i_inpfdc['filesMINIAOD.nevents']) / opts.n_events))
    if njobs == 0:
       KILL(log_prx+'input error: expected number of batch jobs is zero (check input data set and number of events): '+opts.dataset)
    outputname_postfix_format = '_{:0'+str(1+int(math.log10(njobs)))+'d}'
    del njobs

    ### grid certificate
    voms_cert_path = None

    if ('X509_USER_PROXY' in os.environ):
       voms_cert_path = os.environ['X509_USER_PROXY']
    else:
       voms_cert_path = '/tmp/x509up_u'+str(os.getuid())

    if not os.path.isfile(voms_cert_path):
       EXE('voms-proxy-init --voms cms', verbose=opts.verbose, dry_run=opts.dry_run)

    if not os.path.isfile(voms_cert_path):
       KILL(log_prx+'invalid path to voms certificate: '+voms_cert_path)

    EXE('mkdir -p '+OUTPUT_DIR, verbose=opts.verbose, dry_run=opts.dry_run)
    EXE('cp '+voms_cert_path+' '+OUTPUT_DIR+'/X509_USER_PROXY', verbose=opts.verbose, dry_run=opts.dry_run)

    ### copy cmsRun-cfg into output directory
    out_cmsRun_cfg = os.path.abspath(OUTPUT_DIR+'/cfg.py')
    EXE('cp '+opts.cmsRun_cfg+' '+out_cmsRun_cfg, verbose=opts.verbose, dry_run=opts.dry_run)

    if opts.customize_cfg:
       with open(out_cmsRun_cfg, 'a') as cfg_file:
            custom_str = """
###
### customization added by {:} [time-stamp: {:}]
###

import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'Path to python file with content of cms.Process')

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())
"""
            cfg_file.write(custom_str.format(os.path.basename(__file__), str(datetime.datetime.now())))

    ### copy driver command
    with open(os.path.abspath(OUTPUT_DIR+'/cmdLog'), 'w') as file_cmdLog:
         file_cmdLog.write((' '.join(sys.argv[:]))+'\n')

    ### create output batch scripts
    job_counter = 0

    for i_inpfdc in inputfileDicts:

        i_inputFiles = i_inpfdc['filesMINIAOD']
        i_inputFiles_nevents = i_inpfdc['filesMINIAOD.nevents']
        i_secondaryInputFiles = i_inpfdc['filesRAW']

        # number of jobs for this set of input files
        i_njobs = int(math.ceil(float(i_inputFiles_nevents) / opts.n_events))
        i_nevt_remainder = i_inputFiles_nevents%opts.n_events

        for i_job in range(i_njobs):

            # basename of output file without file extension
            i_OUTPUT_BASENAME_woExt = opts.name+outputname_postfix_format.format(job_counter)

            # name of output sub-directory
            i_OUTPUT_DIR = OUTPUT_DIR+'/'+i_OUTPUT_BASENAME_woExt

            # number of events for this job
            i_maxEvents = opts.n_events
            if (i_job == (i_njobs - 1)) and (i_nevt_remainder != 0):
               i_maxEvents = i_nevt_remainder

            # cmsRun arguments (cfg-file + options)
            cmsRun_opts = out_cmsRun_cfg
            cmsRun_opts += ' \\\n maxEvents='+str(i_maxEvents)
            cmsRun_opts += ' \\\n skipEvents='+str(opts.n_events*i_job)
            cmsRun_opts += ' \\\n inputFiles='+str(','.join(i_inputFiles))
            cmsRun_opts += ' \\\n secondaryInputFiles='+str(','.join(i_secondaryInputFiles))
            for _tmp in opts_unknown:
                cmsRun_opts += ' \\\n '+str(_tmp)

            i_SHELL_COMMANDS  = [['set -e']]

            if 'CMSSW_BASE' in os.environ:

               i_SHELL_COMMANDS += [
                 ['cd '+os.environ['CMSSW_BASE']+'/src'],
                 ['eval `scram runtime -sh`'],
               ]

            else:
               KILL(log_prx+'global variable CMSSW_BASE is not defined (set up CMSSW environment with "cmsenv" before submitting jobs)')

            i_SHELL_COMMANDS += [['export X509_USER_PROXY='+OUTPUT_DIR+'/X509_USER_PROXY']]

            i_SHELL_COMMANDS += [['cd '+i_OUTPUT_DIR]]

            i_SHELL_COMMANDS += [['cmsRun '+cmsRun_opts]]

            i_SHELL_COMMANDS += [['touch '+str(i_OUTPUT_BASENAME_woExt)+'.completed']]

            ## dump of full python config
            if job_counter == 0:
               EXE('python '+cmsRun_opts+' dumpPython='+OUTPUT_DIR+'/dumpPython.py &> /dev/null', suspend=False, verbose=opts.verbose, dry_run=opts.dry_run)

            if opts.batch == 'htc':

               batch_job_HTCondor(**{

                 'output_string': '\n\n'.join([' \\\n '.join(_tmp) for _tmp in i_SHELL_COMMANDS]),

                 'output_basename': i_OUTPUT_BASENAME_woExt,

                 'output_directory': i_OUTPUT_DIR,

                 'output_subdirectory': opts.batch,

#                 'transfer_input_files': [OUTPUT_DIR+'/X509_USER_PROXY'],

                 'submit' : opts.submit,

                 'submit_options': opts.htc_opts,

                 'is_slc7_arch': is_slc7_arch,

                 'export_LD_LIBRARY_PATH': (not opts.no_export_LD_LIBRARY_PATH),

                 'RequestCpus': opts.cpus,
                 'RequestMemory': opts.memory,
                 '+RequestRuntime': opts.runtime,

                 'verbose': VERBOSE,

                 'dry_run': opts.dry_run,
               })

            else:
               KILL(log_prx+'unsupported type of batch submission system: '+str(opts.batch))

            job_counter += 1
