self._cmake.definitions['BUILD_opencv_python2'] = False
self._cmake.definitions['BUILD_opencv_python3'] = False
self._cmake.definitions['BUILD_opencv_python_bindings_g'] = False
self._cmake.definitions['BUILD_opencv_python_tests'] = False
self._cmake.definitions['BUILD_opencv_ts'] = False
self._cmake.definitions['WITH_CUFFT'] = False
self._cmake.definitions['WITH_CUBLAS'] = False
self._cmake.definitions['WITH_NVCUVID'] = False
self._cmake.definitions['WITH_FFMPEG'] = False
self._cmake.definitions['WITH_GSTREAMER'] = False
self._cmake.definitions['WITH_OPENCL'] = False
self._cmake.definitions['WITH_CUDA'] = False
self._cmake.definitions['WITH_1394'] = False
self._cmake.definitions['WITH_ADE'] = False
self._cmake.definitions['WITH_ARAVIS'] = False
self._cmake.definitions['WITH_CLP'] = False
self._cmake.definitions['WITH_HALIDE'] = False
self._cmake.definitions['WITH_HPX'] = False
self._cmake.definitions['WITH_IMGCODEC_HDR'] = False
self._cmake.definitions['WITH_IMGCODEC_PFM'] = False
self._cmake.definitions['WITH_IMGCODEC_PXM'] = False
self._cmake.definitions['WITH_IMGCODEC_SUNRASTER'] = False
self._cmake.definitions['WITH_INF_ENGINE'] = False
self._cmake.definitions['WITH_IPP'] = False
self._cmake.definitions['WITH_ITT'] = False
self._cmake.definitions['WITH_LIBREALSENSE'] = False
self._cmake.definitions['WITH_MFX'] = False
self._cmake.definitions['WITH_NGRAPH'] = False
self._cmake.definitions['WITH_OPENCLAMDBLAS'] = False
self._cmake.definitions['WITH_OPENCLAMDFFT'] = False
self._cmake.definitions['WITH_OPENCL_SVM'] = False
self._cmake.definitions['WITH_OPENGL'] = False
self._cmake.definitions['WITH_OPENNI'] = False
self._cmake.definitions['WITH_OPENNI2'] = False
self._cmake.definitions['WITH_OPENVX'] = False
self._cmake.definitions['WITH_PLAIDML'] = False
self._cmake.definitions['WITH_PROTOBUF'] = False
self._cmake.definitions['WITH_PTHREADS_PF'] = False
self._cmake.definitions['WITH_PVAPI'] = False
self._cmake.definitions['WITH_QT'] = False
self._cmake.definitions['WITH_QUIRC'] = False
self._cmake.definitions['WITH_V4L'] = False
self._cmake.definitions['WITH_VA'] = False
self._cmake.definitions['WITH_VA_INTEL'] = False
self._cmake.definitions['WITH_VTK'] = False
self._cmake.definitions['WITH_VULKAN'] = False
self._cmake.definitions['WITH_XIMEA'] = False
self._cmake.definitions['WITH_XINE'] = False
self._cmake.definitions['WITH_LAPACK'] = False
self._cmake.definitions['WITH_IPP_IW'] = False
self._cmake.definitions['WITH_CAROTENE'] = False
self._cmake.definitions['WITH_PROTOBUF'] = False
self._cmake.definitions['WITH_LAPACK'] = False




You can refactor the code using chained assignment as follows:
self._cmake.definitions['BUILD_opencv_python2'] = self._cmake.definitions['BUILD_opencv_python3'] = self._cmake.definitions['BUILD_opencv_python_bindings_g'] = self._cmake.definitions['BUILD_opencv_python_tests'] = self._cmake.definitions['BUILD_opencv_ts'] = self._cmake.definitions['WITH_CUFFT'] = self._cmake.definitions['WITH_CUBLAS'] = self._cmake.definitions['WITH_NVCUVID'] = self._cmake.definitions['WITH_FFMPEG'] = self._cmake.definitions['WITH_GSTREAMER'] = self._cmake.definitions['WITH_OPENCL'] = self._cmake.definitions['WITH_CUDA'] = self._cmake.definitions['WITH_1394'] = self._cmake.definitions['WITH_ADE'] = self._cmake.definitions['WITH_ARAVIS'] = self._cmake.definitions['WITH_CLP'] = self._cmake.definitions['WITH_HALIDE'] = self._cmake.definitions['WITH_HPX'] = self._cmake.definitions['WITH_IMGCODEC_HDR'] = self._cmake.definitions['WITH_IMGCODEC_PFM'] = self._cmake.definitions['WITH_IMGCODEC_PXM'] = self._cmake.definitions['WITH_IMGCODEC_SUNRASTER'] = self._cmake.definitions['WITH_INF_ENGINE'] = self._cmake.definitions['WITH_IPP'] = self._cmake.definitions['WITH_ITT'] = self._cmake.definitions['WITH_LIBREALSENSE'] = self._cmake.definitions['WITH_MFX'] = self._cmake.definitions['WITH_NGRAPH'] = self._cmake.definitions['WITH_OPENCLAMDBLAS'] = self._cmake.definitions['WITH_OPENCLAMDFFT'] = self._cmake.definitions['WITH_OPENCL_SVM'] = self._cmake.definitions['WITH_OPENGL'] = self._cmake.definitions['WITH_OPENNI'] = self._cmake.definitions['WITH_OPENNI2'] = self._cmake.definitions['WITH_OPENVX'] = self._cmake.definitions['WITH_PLAIDML'] = self._cmake.definitions['WITH_PROTOBUF'] = self._cmake.definitions['WITH_PTHREADS_PF'] = self._cmake.definitions['WITH_PVAPI'] = self._cmake.definitions['WITH_QT'] = self._cmake.definitions['WITH_QUIRC'] = self._cmake.definitions['WITH_V4L'] = self._cmake.definitions['WITH_VA'] = self._cmake.definitions['WITH_VA_INTEL'] = self._cmake.definitions['WITH_VTK'] = self._cmake.definitions['WITH_VULKAN'] = self._cmake.definitions['WITH_XIMEA'] = self._cmake.definitions['WITH_XINE'] = self._cmake.definitions['WITH_LAPACK'] = self._cmake.definitions['WITH_IPP_IW'] = self._cmake.definitions['WITH_CAROTENE'] = False