#! /bin/bash

[ "$#" -ne 1 ] && { echo "Usage: $0 <apk_version>"; exit -1; }

mkdir -p build/android/armeabi-v7a
mkdir -p build/android/x86
mkdir -p build/android/all

echo "==================== BUILDING APK FOR armeabi-v7a ======================="

p4a apk --private $PWD/Game --orientation landscape --icon $PWD/Game/assets/icon.png \
        --permission android.permission.INTERNET \
	--presplash Game/assets/start/start_3_0.png \
        --package=org.trumpstamp.trumpstamp --name "TrumpStamp" \
	--dist-name trumpstamp-armeabi-v7a \
        --version $1 --bootstrap=sdl2 --requirements=python2,kivy,pyjnius --arch=armeabi-v7a

mv TrumpStamp-$1-debug.apk build/android/armeabi-v7a

echo "==================== BUILDING APK FOR x86 ======================="

p4a apk --private $PWD/Game --orientation landscape --icon $PWD/Game/assets/icon.png \
	--package=org.trumpstamp.trumpstamp --name "TrumpStamp" \
        --permission android.permission.INTERNET \
	--presplash Game/assets/start/start_3_0.png \
	--dist-name trumpstamp-x86 \
	--version $1 --bootstrap=sdl2 --requirements=python2,kivy,pyjnius --arch=x86

mv TrumpStamp-$1-debug.apk build/android/x86

# echo "==================== MERGING APKS TOGETHER ======================="
#
# unzip build/android/armeabi-v7a/TrumpStamp-$1-debug.apk -d build/android/armeabi-v7a
# rm build/android/armeabi-v7a/TrumpStamp-$1-debug.apk
# unzip build/android/x86/TrumpStamp-$1-debug.apk -d build/android/x86
# rm build/android/x86/TrumpStamp-$1-debug.apk
# cp -r build/android/armeabi-v7a/. build/android/all
# cp -r build/android/x86/. build/android/all
# rm build/android/all/META-INF/CERT.RSA
# rm build/android/all/META-INF/CERT.SF
# cd build/android/all && zip -r TrumpStamp-$1-debug.apk . && mv TrumpStamp-$1-debug.apk .. && cd ../../..
#
# echo "==================== SIGNING FINAL APK ======================="
#
# jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore build/android/TrumpStamp-$1-debug.apk androiddebugkey -storepass android
#
# echo "==================== CLEANING UP ===================="
# rm -rf build/android/all build/android/x86 build/android/armeabi-v7a
