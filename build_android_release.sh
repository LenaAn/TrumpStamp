#! /bin/bash
[ "$#" -ne 5 ] && { echo "Usage: $0 <apk_version> <key_store> <key_name> <store_password> <key_password>"; exit -1; }


rm Game/user.dat
mkdir -p build/android/armeabi-v7a
mkdir -p build/android/x86
#mkdir -p build/android/all

echo "==================== BUILDING APK FOR armeabi-v7a ======================="

p4a apk --private $PWD/Game --orientation landscape --icon $PWD/Game/assets/icon.png \
        --permission android.permission.INTERNET \
	--package=org.trumpstamp.trumpstamp --name "TrumpStamp"\
	--presplash Game/assets/start/start_3_0.png \
	--dist-name trumpstamp-armeabi-v7a --release \
        --version $1 --bootstrap=sdl2 --requirements=python2,kivy --arch=armeabi-v7a \
	--keystore "$2" --signkey $3 --keystorepw $4 --signkeypw $5

mv TrumpStamp-$1-release.apk build/android/armeabi-v7a

echo "==================== BUILDING APK FOR x86 ======================="

p4a apk --private $PWD/Game --orientation landscape --icon $PWD/Game/assets/icon.png \
        --permission android.permission.INTERNET \
	--presplash Game/assets/start/start_3_0.png \
	--package=org.trumpstamp.trumpstamp --name "TrumpStamp" \
	--dist-name trumpstamp-x86 --release \
	--version $1 --bootstrap=sdl2 --requirements=python2,kivy --arch=x86 \
        --keystore "$2" --signkey $3 --keystorepw $4 --signkeypw $5

mv TrumpStamp-$1-release.apk build/android/x86

#echo "==================== MERGING APKS TOGETHER ======================="

#unzip build/android/armeabi-v7a/TrumpStamp-$1-release.apk -d build/android/armeabi-v7a
#rm build/android/armeabi-v7a/TrumpStamp-$1-release.apk
#unzip build/android/x86/TrumpStamp-$1-release.apk -d build/android/x86
#rm build/android/x86/TrumpStamp-$1-release.apk
#cp -r build/android/armeabi-v7a/. build/android/all
#cp -r build/android/x86/. build/android/all
#rm build/android/all/META-INF/CERT.RSA
#rm build/android/all/META-INF/CERT.SF
#cd build/android/all && zip -r TrumpStamp-$1-release.apk . && mv TrumpStamp-$1-release.apk .. && cd ../../..

#echo "==================== SIGNING FINAL APK ======================="

#jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $2 build/android/TrumpStamp-$1-release.apk $3 -storepass $4 -keypass $5

#echo "==================== CLEANING UP ===================="
#rm -rf build/android/all build/android/x86 build/android/armeabi-v7a
