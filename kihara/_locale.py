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
    kihara-link geturl <lien>
        Pour extraire l'URL d'un lien

    kihara-link makelink <url>
        Pour créer un lien depuis une URL
''',
		'INVALID_URL': 'uniquement des caractères imprimables ascii sont autorisés',
		'INVALID_LINK': 'lien non valide',
		'INDEX_MODULE_HELP': '''[Aide pour le module index]

Utilisation :
    kihara-index [nocache] <lien>
        Récupérer et afficher les informations depuis un lien
	no-cache force l'actualisation de l'index 

    kihara-index local <chemin>
        Afficher les informations d'un fichier local
''',
		'LOCAL_INDEX': 'Fichier d\'indexage local {0}',
		'REMOTE_INDEX': 'Fichier d\'indexage distant {0}',
		'INDEX_INFO': 'Informations sur la ressource :',
		'INDEX_NAME': 'Nom :',
		'INDEX_DESCRIPTION': 'Description :',
		'INDEX_RESOURCE_PROVIDER': 'Indexé par :',
		'INDEX_NO_RESOURCE': 'Cet index ne contient pas de ressource',
		'INDEX_UNKNOWN_FIELD': 'Inconnu',
		'INDEX_VERSION': 'Version {0} :',
		'INDEX_SIZE': 'Taille :',
		'INDEX_FRAGMENT': 'Fragment {0} :',
		'INDEX_TYPE': 'Type :',
		'INDEX_LOCATION_PROVIDER': 'Mis en ligne par :',
		'INDEX_HTTPS_LOCATION': 'HTTPS générique',
		'INDEX_HTTP_LOCATION': 'HTTP générique',
		'INDEX_GOOGLE_DRIVE_LOCATION': 'Google Drive',
		'INDEX_LOCATION': 'Emplacement :',
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
    kihara-link geturl <link>
        Extract the URL from a link

    kihara-link makelink <url>
        Create a link from an URL
''',
		'INVALID_URL': 'only printable ascii characters are valid',
		'INVALID_LINK': 'not a valid link',
		'INDEX_MODULE_HELP': '''[Help on the index module]

Usage :
    kihara-index [no-cache] <link>
        Display infos from a link
	no-cache forces the refresh of the index file

    kihara-index local <path>
        Display infos from a local file
''',
		'LOCAL_INDEX': 'Local indexing file {0}',
		'REMOTE_INDEX': 'Remote indexing file {0}',
		'INDEX_INFO': 'Resource informations :',
		'INDEX_NAME': 'Name :',
		'INDEX_DESCRIPTION': 'Description :',
		'INDEX_RESOURCE_PROVIDER': 'Indexed by :',
		'INDEX_NO_RESOURCE': 'This index doesn\'t contain any resource',
		'INDEX_UNKNOWN_FIELD': 'Unknown',
		'INDEX_VERSION': 'Version {0} :',
		'INDEX_SIZE': 'File size :',
		'INDEX_FRAGMENT': 'Fragment {0} :',
		'INDEX_TYPE': 'Type :',
		'INDEX_LOCATION_PROVIDER': 'Uploaded by :',
		'INDEX_HTTPS_LOCATION': 'generic HTTPS',
		'INDEX_HTTP_LOCATION': 'generic HTTP',
		'INDEX_GOOGLE_DRIVE_LOCATION': 'Google Drive',
		'INDEX_LOCATION': 'Location :',
	}

del locale, userlocale
