Pour Beagleboneblack sous Debian 7

puredata à installer d'abord.

Effets spéciaux avec puredata (tremolo, vibrato, drum, reverb, wahwah, etc...)
Un programme en python pedal.py scrupte les boutons de la pédale et envoie à puredata via le port 3010 (pdsend) l'éffet à enclencher.
Certains boutons sont ON/OFF et d'autres sont en push uniquement.

Attention, j'utilise pour lire les 16 entrées pédale, une puce I2C MCP23017. Les entrées ne sont donc pas connectées directement au beaglebone.

J'utilise sur le bbb, une clé usb sound Koenig. Alsa ne fonctionnant pas correctement sur debian/bbb, j'utilise oss pour lancer puredata:
puredata -oss -blocksize 1024 guitareEffects.pd

lancement:
1- puredata
2- pedal.py

