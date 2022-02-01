README
======
This is the README file for the PARSEME verbal multiword expressions (VMWEs) corpus for Turkish, edition 1.2.

The annotated Turkish 1.2 corpus is an updated version of the Turkish PARSEME 1.1 corpus. Changes with respect to the 1.1 version are the following:

* The corpus has been re-parsed using UDPipe, thus completing the missing LEMMA tags in the previous version
* Inconsistent annotations have been resolved
* Missed verbal-MWEs have been annotated

The raw Turkish corpus is introduced newly in edition 1.2. 

The raw corpus is not released in the present directory, but can be downloaded from a [dedicated page](https://gitlab.com/parseme/corpora/-/wikis/Raw-corpora-for-the-PARSEME-1.2-shared-task)

Raw Corpus
-------

Turkish Raw corpus for the 1.2 edition comes from the Turkish newspaper corpus introduced in [Sak et al. (2019)](https://www.cmpe.boun.edu.tr/~gungort/papers/Resources%20for%20Turkish%20Morphological%20Processing.pdf). 

It consists of 
* 1,390,791 sentences,
* 19,463,230 tokens

The corpus has been annotated using UDPipe, relying on the model: turkish-imst-ud-2.4-190531.udpipe

Annotated Corpus
--------------------

Turkish annotated corpus for the 1.2 edition comes from the Turkish newspaper corpus introduced in [1.1 edition](https://www.researchgate.net/publication/326276588_Turkish_verbal_multiword_expressions_corpus). 

The corpus consists of 
* 22,311 sentences, with the following VMWE counts: 
	* LVC.full: 3582 
	* VID: 4139
	* MVC: 5

The corpus has been re-parsed using UDPipe (as opposed to the ITU NLP Tool from edition 1.1, where the LEMMA column was problematic), relying on the model: turkish-imst-ud-2.4-190531.udpipe. 
After the dependency parser, previous annotations from edition 1.1 (which relied on the PARSEME Shared Task on Automatic Identification of Verbal Multiword Expressions 1.1 Guidelines) have been copied, and MWEs that have been missed, have been annotated. 

Provided annotations
--------------------
The data are in the [.cupt](http://multiword.sourceforge.net/cupt-format) format. Here is detailed information about some columns:

* LEMMA (column 3): Available. Automatically annotated (UDPipe).
* UPOS (column 4): Available. Automatically annotated (UDPipe).
* FEATS (column 6): Available. Automatically annotated (UDPipe).
* HEAD and DEPREL (columns 7 and 8): Available. Automatically annotated (UDPipe).
* MISC (column 10): No-space information available. Automatically annotated. (UDPipe).
* PARSEME:MWE (column 11): Manually annotated. The following [VMWE categories](http://parsemefr.lif.univ-mrs.fr/parseme-st-guidelines/1.1/?page=030_Categories_of_VMWEs) are annotated: LVC.full, VID, MVC.


Authors
-------
Language Leader: Tunga Güngör (contact: gungort@boun.edu.tr)
The annotation team consists of the following 9 members: 
* Edition 1.2: Tunga Güngör, Zeynep Yirmibeşoğlu 
* Edition 1.1: Tunga Güngör, Berna Erden, Gözde Berk
* Edition 1.0: Gülşen Eryiğit, Kübra Adalı, Tutkum Dinç, Ayşenur Miral, Mert Boz



Copyright information
---------------------
Creative Commons  CC-BY-NC-SA License.
https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode


Citation information
--------------------
Please refer to the following publication while using the Turkish annotated dataset:
@InProceedings{turkishdataset,
  author = {Berna Erden, Gozde Berk, and Tunga Gungor},
  title = {Turkish Verbal Multiword Expressions Corpus},
  booktitle = {26th IEEE Signal Processing and Communications Applications Conference, SIU 2018},
  month = {May},
  year = {2018},
  address = {İzmir, Turkey},
  pages={1-4}
  doi={10.1109/SIU.2018.8404583}
}

Licence
-------
The full dataset is licensed under Creative Commons Non-Commercial Share-Alike 4.0 licence CC-BY-NC-SA 4.0


References
----------
@InProceedings{itunlp,
  author = {Eryigit, Gulsen},
  title = {ITU Turkish NLP Web Service},
  booktitle = {Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics (EACL)},
  month = {April},
  year = {2014},
  address = {Gothenburg, Sweden},
  publisher = {Association for Computational Linguistics},
}

@InProceedings{udturkish,
  author    = {Sulubacak, Umut  and  Gokirmak, Memduh  and  Tyers, Francis  and  Coltekin, Cagri  and  Nivre, Joakim  and  Eryigit, Gulsen},
  title     = {Universal Dependencies for Turkish},
  booktitle = {Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics},
  month     = {December},
  year      = {2016},
  address   = {Osaka, Japan},
  publisher = {The COLING 2016 Organizing Committee},
  pages     = {3444--3454},
  url       = {http://aclweb.org/anthology/C16-1325}
}

@article{10.2307/41486039,
 ISSN = {1574020X, 15728412},
 URL = {http://www.jstor.org/stable/41486039},
 author = {Haşim Sak and Tunga Güngör and Murat Saraçlar},
 journal = {Language Resources and Evaluation},
 number = {2},
 pages = {249--261},
 publisher = {Springer},
 title = {Resources for Turkish morphological processing},
 volume = {45},
 year = {2011}
}


