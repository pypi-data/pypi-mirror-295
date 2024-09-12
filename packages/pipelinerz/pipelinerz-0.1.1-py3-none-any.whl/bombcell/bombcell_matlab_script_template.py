bombcell_template_matlab_script= """
fprintf('running template bombcell script')\n
gain_to_uV = 0.195; \n
fprintf('bc_loadEphysData')\n

[spikeTimes_samples, spikeTemplates, templateWaveforms, templateAmplitudes, pcFeatures, pcFeatureIdx, channelPositions] = bc_loadEphysData(ephysKilosortPath);\n
fprintf('bc_loadEphysData done')\n
fprintf('bc_manageDataCompression')\n
rawFile = bc_manageDataCompression(ephysRawDir, decompressDataLocal);\n
fprintf('bc_manageDataCompression')\n

fprintf('bc_qualityParamValuesForUnitMatch')\n

%param = bc_qualityParamValues(ephysMetaDir, rawFile, ephysKilosortPath, gain_to_uV);\n 
param = bc_qualityParamValuesForUnitMatch(ephysMetaDir, rawFile); % Run this if you want to use UnitMatch after\n
fprintf('bc_qualityParamValuesForUnitMatch done')\n

rerun = 0; \n
fprintf('qmetrics')\n

qMetricsExist = ~isempty(dir(fullfile(savePath, 'qMetric*.mat'))) || ~isempty(dir(fullfile(savePath, 'templates._bc_qMetrics.parquet')));\n
\n


if qMetricsExist == 0 || rerun\n
    fprintf('running bc_runAllQualityMetrics')\n
    [qMetric, unitType] = bc_runAllQualityMetrics(param, spikeTimes_samples, spikeTemplates, templateWaveforms, templateAmplitudes,pcFeatures,pcFeatureIdx,channelPositions, savePath); \n
else\n
    fprintf('loading previous bc_runAllQualityMetrics')\n

    [param, qMetric] = bc_loadSavedMetrics(savePath);\n 
    unitType = bc_getQualityUnitType(param, qMetric, savePath);\n
end\n
\n
original_id_we_want_to_load = 0;\n
id_we_want_to_load_1_indexed = original_id_we_want_to_load + 1;\n 
number_of_spikes_for_this_cluster = qMetric.nSpikes(qMetric.clusterID == id_we_want_to_load_1_indexed);\n
original_id_we_want_to_load = 0;\n
number_of_spikes_for_this_cluster = qMetric.nSpikes(qMetric.phy_clusterID == original_id_we_want_to_load);\n
\n
goodUnits = unitType == 1;\n
muaUnits = unitType == 2;\n
noiseUnits = unitType == 0;\n
nonSomaticUnits = unitType == 3;\n 
\n
all_good_units_number_of_spikes = qMetric.nSpikes(goodUnits);\n
\n
label_table = table(unitType);\n
writetable(label_table,[savePath filesep 'templates._bc_unit_labels.tsv'],'FileType', 'text','Delimiter','\t');\n
\n
"""
