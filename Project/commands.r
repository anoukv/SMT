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

correctie:
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/random_model_legal/ -corpus results/random.legal -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/random.legal.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/random_model_software/ -corpus results/random.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/random.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40

/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/svm_model_legal/ -corpus results/svm_results.legal -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/svm_results.legal.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/svm_model_software/ -corpus results/svm_results.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/svm_results.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40

/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/wbs_model_legal/ -corpus results/wbs_results.legal -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/wbs_results.legal.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40
/apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/wbs_model_software/ -corpus results/wbs_results.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/wbs_results.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40

# /apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/random_model_software/ -corpus results/random.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/random.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40
# /apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/svm_model_software/ -corpus results/svm_results.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/svm_results.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40

# /apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/wbs_model_legal/ -corpus results/wbs_results.legal -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/wbs_results.legal.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40
# /apps/smt_tools/decoders/mosesdecoder/scripts/training/train-model.perl -root-dir models/wbs_model_software/ -corpus results/wbs_results.software -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:/home/avisser/data/lm/wbs_results.software.en.lm:8 -external-bin-dir /apps/smt_tools/alignment/mgizapp-0.7.3/manual-compile -mgiza -mgiza-cpus 40


VERTALINGEN:
/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/random_model_legal/model/moses.ini -input-file legal.test.es > translations/random.legal.test.en;
/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/random_model_software/model/moses.ini -input-file software.test.es > translations/random.software.test.en;

/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/svm_model_legal/model/moses.ini -input-file legal.test.es > translations/svm_results.legal.test.en;
/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/svm_model_software/model/moses.ini -input-file software.test.es > translations/svm_results.software.test.en;

/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/wbs_model_legal/model/moses.ini -input-file legal.test.es > translations/wbs_results.legal.test.en;
/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/wbs_model_software/model/moses.ini -input-file software.test.es > translations/wbs_results.software.test.en;

/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/random_model_software/model/moses.ini -input-file software.test.es > translations/random.software.test.en;

/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/svm_model_software/model/moses.ini -input-file software.test.es > translations/svm_results.software.test.en;

/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/wbs_model_legal/model/moses.ini -input-file legal.test.es > translations/wbs_results.legal.test.en;
/apps/smt_tools/decoders/mosesdecoder/bin/moses -config models/wbs_model_software/model/moses.ini -input-file software.test.es > translations/wbs_results.software.test.en;



BLEU SCORE:
/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc legal.test.en < translations/random.legal.test.en
/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc software.test.en < translations/random.software.test.en

/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc legal.test.en < translations/svm_results.legal.test.en
/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc software.test.en < translations/svm_results.software.test.en

/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc legal.test.en < translations/wbs_results.legal.test.en
/apps/smt_tools/decoders/mosesdecoder/scripts/generic/multi-bleu.perl -lc software.test.en < translations/wbs_results.software.test.en



