lsusb
gphoto2 --auto-detect
gphoto2 --summary
gphoto2 --list-config
gphoto2 --capture-image-and-download
gphoto2 --capture-image-and-download --filename "prout.jpg"
gphoto2 --get-config=/main/status/batterylevel # works even if camera is sleeping
gphoto2 --get-config=/main/actions/autofocusdrive # also useful to wake-up camera
gphoto2 --get-config=/main/status/cameramodel
gphoto2 --get-config=/main/imgsettings/iso | grep Current
gphoto2 --get-config=/main/status/lensname
gphoto2 --get-config=/main/capturesettings/aperture
gphoto2 --list-files
gphoto2 --get-all-files