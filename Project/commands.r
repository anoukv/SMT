http://www.statmt.org/moses/?n=FactoredTraining.TrainingParameters

LM:
vanaf home/avisser/data/
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/wbs_results.software.es -lm lm/wbs_results.software.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/wbs_results.legal.es -lm lm/wbs_results.legal.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/wbs_results.software.en -lm lm/wbs_results.software.en.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/wbs_results.legal.en -lm lm/wbs_results.legal.en.lm

/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/random.software.es -lm lm/random.software.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/random.legal.es -lm lm/random.legal.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/random.software.en -lm lm/random.software.en.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/random.legal.en -lm lm/random.legal.en.lm

/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/svm_results.software.es -lm lm/svm_results.software.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/svm_results.legal.es -lm lm/svm_results.legal.es.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/svm_results.software.en -lm lm/svm_results.software.en.lm
/apps/lm_tools/srilm-1.7/bin/i686-m64/ngram-count -order 3 -interpolate -kndiscount -unk -text results/svm_results.legal.en -lm lm/svm_results.legal.en.lm

ALLIGNMENTS:
vanaf home/avisser/data/workingdir/
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/random_model_legal/ --f es --e en --corpus results/random.legal -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/random.legal.en.lm
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/random_model_software/ --f es --e en --corpus results/random.software -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/random.software.en.lm

/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/svm_model_legal/ --f es --e en --corpus results/svm_results.legal -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/svm_results.legal.en.lm
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/svm_model_software/ --f es --e en --corpus results/svm_results.software -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/svm_results.software.en.lm

/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/wbs_model_legal/ --f es --e en --corpus results/wbs_results.legal -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/wbs_results.legal.en.lm
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl --root-dir models/wbs_model_software/ --f es --e en --corpus results/wbs_results.software -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40 -lm 0:3:/home/avisser/data/lm/wbs_results.software.en.lm

/apps/smt_tools/decoders/mosesdecoder/moses-cmd/bin/gcc-4.8/release/debug-symbols-on/link-static/threading-multi/moses -config models/random_model_legal/model/moses.ini -input-file legal.test.en > translations/random.legal.test.en;