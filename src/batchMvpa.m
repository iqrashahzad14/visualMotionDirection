clear ;
clc;

%% set paths
  % spm
  warning('off');
  addpath(genpath('/Users/battal/Documents/MATLAB/spm12'));
  % cosmo
  cosmo = '~/Documents/MATLAB/CoSMoMVPA';
  addpath(genpath(cosmo));
  cosmo_warning('once');

  % libsvm
  libsvm = '~/Documents/MATLAB/libsvm';
  addpath(genpath(libsvm));
  % verify it worked.
  cosmo_check_external('libsvm'); % should not give an error
  
  % add cpp repo
  run ../../rhythmBlock_fMRI_analysis/lib/CPP_BIDS_SPM_pipeline/initCppSpm.m;
  
     
  % load your options
  opt = getOptionBlockMvpa();

  %% run mvpa 
  
  % use parcels or NS masks?
  roiSource = 'hmat'; % 'freesurfer', 'neurosynth', ...
  accuracy = calculateMvpa(opt, roiSource);
  
  
  
  
  