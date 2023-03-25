---
title: Ubuntu 14.04 не загружается после установки на ноутбук Sony Vaio с UEFI и предустановелнной Windows 7
date: 2015-02-22 13:02:27 +0300
draft: false
tags: [old-site, Ubuntu, загрузка, UEFI, Windows 7]
---
Проблема: Ubuntu 14.04 корректно устанавливается на ноутбук Sony Vaio с UEFI и предустановленной Windows 7, но загрузки ОС не происходит, по прежнему грузится только Windows без возможности выбрать другую ОС. Использование из-под Ubuntu (live cd/usb) boot-repair и с дефолтными, и с кастомными настройками не помогают:
```
sudo add-apt-repository -y ppa:yannubuntu/boot-repair && sudo apt-get update    
sudo apt-get install -y boot-repair && boot-repair
```

Выполнение из-под Windows команды:
```
bcdedit /set {bootmgr} path \EFI\ubuntu\shimx64.efi
```

не помогает.

Нагуглил тут: http://askubuntu.com/questions/150174/sony-vaio-with-insyde-h2o-efi-bios-will-not-boot-into-grub-efi/150640#150640 и тут: http://askubuntu.com/questions/159918/cant-dual-boot-ubuntu-12-04-and-windows-7-on-sony-vaio-s-15-2012, что проблема может быть в том, что виндовый лоадер захардкожен в прошивке ноутбука. По этому проблема решилась заменой виндового `.efi` файла аналогичным убунтовским (из-под Ubuntu live cd и с предварительным бэкапом первого файла, конечно):
```
sudo su
mkdir -p /mnt/efi_partition
mount -t vfat /dev/sda3  /mnt/efi_partition
cd /mnt/efi_partion/EFI/Microsoft/Boot
cp bootmgfw.efi bootmgfw.efi.old
cp /mnt/efi_partition/EFI/ubuntu/grubx64.efi bootmgfw.efi
update-grub
reboot
```

В моем случае больше ничего не понадобилось, но, возможно, потребуется добавить Windows в настройки Grub, для этого в файл `/etc/grub.d/40_custom` надо добавить:
```
menuentry "Windows 7" {
    set root='(hd0,gpt3)'
    chainloader /EFI/Boot/bootx64.efi
}
```
И обновить настройки:
```
update-grub
```
Ну и, напоследок, может захотеться поменять порядок загрузки ОС, для этого в `/etc/default/grub` параметру `GRUB_DEFAULT` нужно присвоить номер ОС в списке систем, который появляется при загрузке компьютера (и опять не забыть выполнить update-grub).

**Update**

После установки очередного апдейта винда затерла лоадер своим дефотным и Убунту перестала грузиться, а флешки с Убунтой, для того чтобы проделать описанные выше действия не оказалось, поэтому я нашел способ восстановить лоадер из-под винды:
```
mountvol K: /S
```
(вместо K: можно подставить любую неиспользуюмую в именах дисков букву). Далее из-под админа копируем файл `grubx64.efi` на место `bootmgfw.efi` как это указано в примере с Убунту.
<!--more-->

