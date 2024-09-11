FILE_TYPES = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt', '.md', '.tex', '.epub', '.pages'],
    'Spreadsheets': ['.xls', '.xlsx', '.ods', '.csv'],
    'Presentations': ['.ppt', '.pptx', '.odp', '.key'],
    'Images': ['.avif', '.jpg', '.jpeg', '.jpg_large', '.png', '.gif', '.bmp', '.tiff', '.svg', '.eps', '.ico', '.webp', '.heic', '.raw', '.indd', '.jfif', '.hdr'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.mpeg', '.mpg', '.m4v', '.3gp', '.vob', '.ogv'],
    'Audios': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma', '.alac', '.aiff', '.amr', '.8svx'],
    'Archives': ['.zip', '.tar', '.rar', '.7z', '.gz', '.bz2', '.xz', '.dmg', '.tgz', '.cab'],
    'Code': ['.py', '.java', '.c', '.cpp', '.js', '.html', '.css', '.sass', '.scss', '.json', '.xml', '.yaml', '.yml', '.php', '.rb', '.go', '.rs', '.sh', '.bat', '.cmd', '.sql', '.kt', '.ts', '.vue'],
    'Executables': ['.exe', '.msi', '.apk', '.run', '.appimage', '.jar', '.deb', '.rpm', '.pkg'],
    'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon'],
    'Ebooks': ['.mobi', '.azw3', '.fb2', '.lit', '.ibooks', '.cbr', '.cbz'],
    'Database': ['.sql', '.sqlite', '.db', '.mdb', '.accdb'],
    '3D-Models': ['.skp', '.gltf', '.usdz', '.t3d', '.mtl', '.vox', '.obj', '.stl', '.fbx', '.blend', '.blend1', '.dae', '.3ds', '.max', '.c4d', '.glb'],
    'CAD-Models': ['.dwg', '.dxf', '.step', '.stp', '.iges', '.igs', '.sldprt', '.sldasm', '.prt', '.asm'],
    'Virtual-Disks': ['.vhd', '.vhdx', '.vdi', '.vmdk', '.qcow2'],
    'Scripts': ['.pl', '.rb', '.r', '.lua', '.vbs'],
    'System-Files': ['.sys', '.ini', '.dll', '.cfg', '.log', '.tmp', '.dat', '.bak'],
    'Web-Files': ['.htm', '.asp', '.aspx', '.jsp'],
    'Configurations': ['.conf', '.toml', '.env'],
    'Audiobooks': ['.m4b', '.aa', '.aax'],
    'Podcasts': ['.pod'],
    'Subtitles': ['.srt', '.sub', '.ass', '.ssa', '.vtt'],
    'Disk-Images': ['.img', '.cue', '.iso', '.bin'],
    'Game-ROMs': ['.rom', '.gcm', '.gba', '.gb', '.gbc', '.z64', '.sms', '.nes', '.smd', '.pce', '.chd', '.n64', '.smc', '.sfc', '.a26', '.a8', '.dsk'],
    'Design': ['.aseprite', '.aseprite-extension', '.fig', '.sketch'],
    'Adobe': ['.prproj', '.psd', '.ai', '.xd'],
    'Unreal-Engine': ['.uasset', '.mhb'],
    'Shortcuts': ['.lnk'],
    'Others': ['.tps'],
    'Folders': []
}

EXCLUDED_DIRECTORIES_WINDOWS = {
    'C:\\Windows',
    'C:\\Program Files',
    'C:\\Program Files (x86)',
    'C:\\$Recycle.Bin',
    'C:\\System Volume Information',
    'C:\\pagefile.sys',
    'C:\\hiberfil.sys'
}

SYSTEM_USER_DIRECTORIES_WINDOWS = {
    'Default',
    'Default User',
    'Public'
}

EXCLUDED_DIRECTORIES_MAC = {
    '/System',
    '/Library',
    '/Applications',
    '/Volumes',
    '/.Trash',
    '/private',
    '/var',
    '/tmp'
}

SYSTEM_USER_DIRECTORIES_MAC = {
    'Shared',
    'Guest'
}

EXCLUDED_DIRECTORIES_LINUX = {
    '/bin',
    '/sbin',
    '/lib',
    '/lib64',
    '/usr/bin',
    '/usr/sbin',
    '/usr/lib',
    '/usr/lib64',
    '/etc',
    '/dev',
    '/proc',
    '/sys',
    '/home',
    '/tmp',
    '/var',
    '/root'
}

SYSTEM_USER_DIRECTORIES_LINUX = {
    'nobody',
    'daemon',
    'mail',
    'ftp',
    'www-data',
    'systemd-network',
    'systemd-resolve'
}