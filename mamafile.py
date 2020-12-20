import mama
class opencv(mama.BuildTarget):
    def dependencies(self):
        pass

    def configure(self):
        opt = [
            "ENABLE_PRECOMPILED_HEADERS=ON", "ENABLE_CCACHE=ON",
            "ENABLE_PYLINT=OFF", "ENABLE_FLAKE8=OFF", "ENABLE_COVERAGE=OFF",

            "BUILD_DOCS=OFF",    "BUILD_EXAMPLES=OFF",        "BUILD_TESTS=OFF", "BUILD_PERF_TESTS=OFF",
            "BUILD_PACKAGE=OFF", "BUILD_ANDROID_SERVICE=OFF", "BUILD_JAVA=OFF",  "PYTHON_DEFAULT_AVAILABLE=OFF",
            "BUILD_OPENEXR=OFF", "BUILD_TIFF=OFF", "BUILD_JPEG=ON", "BUILD_OPENJPEG=ON", "BUILD_ANDROID_PROJECTS=OFF",
            "BUILD_PNG=ON",      "BUILD_ZLIB=ON",  "BUILD_JASPER=OFF", "BUILD_ANDROID_EXAMPLES=OFF",

            "WITH_OPENGL=ON",    "WITH_IPP=OFF",   "WITH_OPENCL=OFF",  "WITH_1394=OFF",
            "WITH_CUDA=OFF",     "WITH_OPENGL=ON", "WITH_JASPER=OFF",  "WITH_WEBP=OFF",
            "WITH_OPENEXR=OFF",  "WITH_TIFF=OFF",  "WITH_LAPACK=OFF",  "WITH_MATLAB=OFF",

            "BUILD_opencv_apps=OFF",      "BUILD_opencv_calib3d=ON",   "BUILD_opencv_core=ON",
            "BUILD_opencv_features2d=ON", "BUILD_opencv_flann=ON",     "BUILD_opencv_highgui=ON",
            "BUILD_opencv_imgcodecs=ON",  "BUILD_opencv_imgproc=ON",   "BUILD_opencv_ml=ON",
            "BUILD_opencv_objdetect=ON",  "BUILD_opencv_photo=ON",     "BUILD_opencv_shape=OFF",
            "BUILD_opencv_stitching=OFF", "BUILD_opencv_superres=OFF", "BUILD_opencv_ts=OFF",
            "BUILD_opencv_video=ON",      "BUILD_opencv_videoio=ON",   "BUILD_opencv_videostab=ON",
            "BUILD_opencv_nonfree=OFF",   "BUILD_SHARED_LIBS=OFF",     "BUILD_opencv_java=OFF", 
            "BUILD_opencv_python2=OFF",   "BUILD_opencv_python3=OFF",  "BUILD_opencv_xphoto=ON",
            "BUILD_opencv_dnn=ON",        "BUILD_opencv_ml=ON",

            "BUILD_opencv_world=ON"
        ]
        if   self.android: opt += ['BUILD_ANDROID_EXAMPLES=OFF', 'BUILD_opencv_androidcamera=ON', 'WITH_FFMPEG=OFF']
        elif self.ios:     opt += ['IOS_ARCH=arm64', 'WITH_FFMPEG=OFF']
        elif self.windows: opt += ['BUILD_WITH_STATIC_CRT=OFF', 'WITH_FFMPEG=OFF', 
                                    'CPU_BASELINE=SSE4_1', 'CPU_DISPATCH=AVX,AVX2']
        elif self.macos:   opt += ['WITH_GSTREAMER=OFF', 'WITH_GPHOTO2=OFF', 'WITH_FFMPEG=OFF']
        elif self.linux:   opt += ['WITH_GSTREAMER=OFF', 'WITH_GPHOTO2=OFF', 'WITH_FFMPEG=ON', 
                                   'WITH_GTK=ON', 'WITH_GTK_2_X=OFF', 'HAVE_GTK3=OFF']
        self.add_cmake_options(opt)
        self.cmake_build_type = 'Release'
        self.cmake_ios_toolchain = 'platforms/ios/cmake/Toolchains/Toolchain-iPhoneOS_Xcode.cmake'
        if self.android:
            self.add_cxx_flags('-I/')
        if self.windows:
            self.add_cl_flags('/wd4819')
        if self.linux:
            self.add_cl_flags('-mfma')
        if self.ios:
            self.disable_ninja_build() # opencv for ios blows up with Ninja

    def package(self):
        if self.android:
            self.export_libs('sdk/native/staticlibs', ['.a'])
            self.export_libs('sdk/native/3rdparty/libs')
            self.export_include('sdk/native/jni/include', build_dir=True)
        else:
            self.export_libs('lib', ['.a', '.lib'], order=['opencv'])
            self.export_libs('3rdparty/lib')
            self.export_include('include', build_dir=True)

        if self.macos or self.ios:
            self.export_syslib("-framework Foundation")
            self.export_syslib("-framework CoreGraphics")
            self.export_syslib("-framework CoreMedia")
            self.export_syslib("-framework CoreVideo")
            self.export_syslib("-framework AVFoundation")
            self.export_syslib("-framework CoreImage")
            if self.ios:
                self.export_syslib("-framework UIKit")
                self.export_syslib('-framework OpenGLES')
            if self.macos:
                self.export_syslib("-framework AppKit")
                self.export_syslib('-framework OpenGL')
        elif self.android:
            self.export_syslib("m")
            self.export_syslib("camera2ndk")
            self.export_syslib("mediandk")
            self.export_syslib("GLESv3")
            self.export_syslib("EGL")
        elif self.windows:
            self.export_syslib('opengl32.lib')
            self.export_syslib("Vfw32")
        elif self.linux:
            self.export_include('include/opencv4', build_dir=True)
            self.export_syslib('GL', 'libgl1-mesa-dev') # libGL.so
            # !!!! required for GUI !!!!
            self.export_syslib('gtk-3', 'libgtk-3-dev')
            self.export_syslib('gdk-3', 'libgtk-3-dev')
            self.export_syslib('cairo', 'libcairo2-dev')
            #self.export_syslib('gtkglext-x11-1.0', 'libgtkglext1 libgtkglext1-dev')
            #self.export_syslib('gdkglext-x11-1.0', 'libgtkglext1 libgtkglext1-dev')
            self.export_syslib('gdk_pixbuf-2.0', 'libglib2.0-dev')
            self.export_syslib('gobject-2.0', 'libglib2.0-dev')
            self.export_syslib('glib-2.0', 'libglib2.0-dev')
            #self.export_syslib('gtk-x11-2.0', 'libgtk-2.0-dev')


