def __getattr__(attr):
	return TEXT.get(attr, '$'+attr)

import locale
userlocale = locale.getdefaultlocale()[0].upper()

if userlocale.startswith('FR'):
	TEXT = {
		'MAIN_INFO_MSG': '''
Outils :

    kihara-download (ou python3 -m kihara.download)
        Télécharger des fichiers distants

    kihara-hide (ou python3 -m kihara.hide)
        Cacher des fichiers

    kihara-extract (ou python3 -m kihara.extract)
        Restaurer des fichiers chachés

    kihara-index (ou python3 -m kihara.index)
        Afficher le contenu de fichiers d'indexage (.kri)

    kihara-link (ou python3 -m kihara.link)
        Opérations sur les liens kihara
''',
		'LINK_MODULE_HELP': '''[Aide pour le module link]

Utilisation :
    kihara-link get-url <lien>
        Pour extraire l'URL d'un lien

    kihara-link make-link <url>
        Pour créer un lien depuis une URL
''',
		'INVALID_URL': 'URL non valide',
		'INVALID_LINK': 'lien non valide',
		'INDEX_MODULE_HELP': '''[Aide pour le module index]

Utilisation :
    kihara-index <lien>
        Récupérer et afficher les informations depuis un lien

    kihara-index local <chemin>
        Afficher les informations d'un fichier local
''',
		'INDEX_INFO': 'Informations sur la ressource :',
		'INDEX_NAME':              'Nom           :',
		'INDEX_DESCRIPTION':       'Description   :',
		'INDEX_RESOURCE_PROVIDER': 'Indexé par    :',
		'INDEX_NO_RESOURCE': 'Cet index ne contient pas de ressource',
		'INDEX_UNKNOWN_FIELD': 'Inconnu',
		'INDEX_VERSION':         'Version {0}     :',
		'INDEX_SIZE':              'Taille        :',
		'INDEX_LOCATION':        'Emplacement {0} :',
		'INDEX_TYPE':              'Type          :',
		'INDEX_LOCATION_PROVIDER': 'Fourni par    :',
		'INDEX_DATE':              'Mise en ligne :',
		'INDEX_HTTPS_LOCATION': 'HTTPS générique',
		'INDEX_HTTP_LOCATION': 'HTTP générique',
		'INDEX_GOOGLE_DRIVE_LOCATION': 'Google Drive',
		'INDEX_FRAGMENT':        'Fragment {0}    :',
	}
else:
	TEXT = {
		'MAIN_INFO_MSG': '''
Tools :

    kihara-download (or python3 -m kihara.download)
        Download remote files

    kihara-hide (or python3 -m kihara.hide)
        Hide files

    kihara-extract (or python3 -m kihara.extract)
        Recover hidden files

    kihara-index (or python3 -m kihara.index)
        Display indexing files (.kri) data

    kihara-link (or python3 -m kihara.link)
        Kihara links manipulation
''',
		'LINK_MODULE_HELP': '''[Help on the link module]

Usage :
    kihara-link get-url <link>
        Extract the URL from a link

    kihara-link make-link <url>
        Create a link from an URL
''',
		'INVALID_URL': 'not a valid URL',
		'INVALID_LINK': 'not a valid link',
		'INDEX_MODULE_HELP': '''[Help on the index module]

Usage :
    kihara-index <link>
        Display infos from a link

    kihara-index local <path>
        Display infos from a local file
''',
	}

del locale, userlocale