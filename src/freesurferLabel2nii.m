
% vistasoft toolbox
addpath(genpath('~/Documents/MATLAB/vistasoft'));
%addpath(genpath('~/Documents/MATLAB/vistasoft/fileFilters'));

subID ='001';
labelName = 'rh.BA6_exvivo';

subjectPath = '/Users/battal/Cerens_files/fMRI/Processed/RhythmCateg/RhythmCateg_Anat/fs_output/';
labelFileName = fullfile(subjectPath, subID, 'label',[labelName,'.label']);
niftiRoiName = fullfile(subjectPath, subID, 'label',labelName); 
regMgzFile = fullfile(subjectPath, subID, 'mri','rawavg.mgz');

% [niftiRoiName, niftiRoi] = fs_labelFileToNiftiRoi(fs_subject,labelFileName,niftiRoiName,[hemisphere],[regMgzFile],[smoothingKernel])


fs_labelFileToNiftiRoi(subID,labelFileName,niftiRoiName,[],regMgzFile);