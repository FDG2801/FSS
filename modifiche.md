- modificata riga 75 argparser: aggiunto isic
```parser.add_argument("--dataset", type=str, default='voc',
                        choices=['voc', 'coco', 'coco-stuff','isic'], help='Name of dataset')```
- **in FSS/dataset/ aggiunto file isic.py -- da testare**
- in "_init.py__" aggiunto le seguenti: 
	from .isic import ISICDataset (come import librerie)
	riga 38 aggiunto questo (scelta dataset):
```elif opts.dataset == 'voc' or 'coco' or 'isic' in opts.dataset:
        if opts.dataset == 'voc':
            dataset = VOCFSSDataset
        else:   
            if opts.dataset == 'isic': 
                dataset = ISICDataset
            else:
                if 'stuff' in opts.dataset:
                    dataset = COCOStuffFSS
                else:
                    dataset = COCOFSS```
- idealmente il comando per runnarlo sarebbe:
```!bash python -m torch.distributed.launch --master_port 2671 --nproc_per_node=1 /content/FSS/run_isic.py --local-rank 0 --data_root /content/FSS/data/ --no_pretrained --backbone resnet50 --task 5-1```
!! run.py e run_isic.py sono uguali !!
- aggiunta in /data/ "isic_tiny" che contiene una versione ridotta di isic 
- creata la cartella split con dentro train (contiene i nomi delle immagini del training) e val
- al momento ho supporto che labels (che è presente in tutti i dataset) siano le gt, e quindi ho creato labels.txt con quei dati; tuttavia quando si runna il programma non sembra essere influente
- make_annotation_isic.py -> dubbio se mettere path completo o meno
- utils_isic.py contiene due funzioni che hanno creato train.txt e val.txt

## Aggiornamento Giugno

- ho deciso di prendere il dataset con cui funziona e cercare di replicare 1:1 con il dataset isic: PascalVOC12 è l'attuale dataset voc con cui funziona, ed è diviso come segue:
	- Annotations => contiene 17125 elementi xml che se aperti danno informazioni sulla immagine, in particolar modo:
		- folder, filename, database, size (h,w, depth), segmented (?), object (name, pose, truncated (?), difficult (?)), coordinate della bounding box, parte del corpo (che parte, dimensioni, coordinate)
	- ImageSets, divisa in 
		- Action che è una serie di file txt con il formato <<nome_immagine task>>, tranne per i file train.txt, trainval.txt, val.txt che hanno i nomi dei file 
		- Layout che ha i nomi dei file nel formato <<nome_immagine labelDiAppartenenza>> per train, trainval e val 
		- Main che ha dei file txt immagino per tutte le classi con i nomi dell'immagine e un numero (1 o -1)
		- Segmentation che ha train, trainval e val come file di testo dove sono contenuti i nomi delle immagini prese in considerazione
	- JPEGImages che ha una serie di immagini jped da segmentare immagino, perché sono come foto scattate
	- SegmentationClass praticamente sembrano essere le immagini di JPEGImages segmentate e con gli oggetti (al plurale) rilevati
	- SegmentationClassAug come sopra ma sembrano esserci solo le bounding box e nonostante ci sia una divisione per oggetto, non ci sono i colori diversi
	- SegmentationClassAug_Visualization mi sembra uguale a SegmentationClass
	- SegmentationObject divisione per oggetti, che sono distinti
	- splits ha i path delle immagini 
	
Il dataset è evidentemente molto diverso e continuo a cercare di capire se si possa effettivamente applicare il modello ad isic. 

Idealmente se dovessi replicare quello che farei è:

- Annotations => più che gli xml, potrei mettere i json
- ImagesSets:
	- Action conterrebbe <<nome_immagine task>> dove task semplicemente sarebbe il nome di tutte le immaigni affiancato da 1-1 e 1-2, poi train.txt, trainval.txt e val.txt posso farli con solo i nomi dei file senza problemi
	- Layout, anche questo credo sia fattibile, ovviamente le label sarebbero solo 0 e 1 (melanoma o sebhorreic) 
	- Main, dovrei capire cosa sono 1 e -1 ma penso siano "è di quella classe se è 1 e non lo è se è -1", quindi potrebbe essere fattibile
	- Segmentation dovrebbe essere facilmente replicabile
	- JPEGImages le immagini "normali"
	In tutte le altre cartelle andrei a mettere praticamente le stesse foto, visto che non ci sono immagini con oggetti distinti in quanto c'è solo un tumore
	- splits, fattibile credo 

Prima di procedere però mi piacerebbe avere un parere su quello che ho detto, nel senso se è fattibile o meno 

DATASET FSS1000:

Non sono riuscito a trovare una resnet addestrata su fss1000 o una porzione di fss1000, ho guardato il dataset ed è diviso per cartelle (ogni cartella è una classe) in cui i file jpg rappresnetano l'oggetto e i file png rappresentano l'oggetto segmentato.
Non saprei bene come adattare questo

