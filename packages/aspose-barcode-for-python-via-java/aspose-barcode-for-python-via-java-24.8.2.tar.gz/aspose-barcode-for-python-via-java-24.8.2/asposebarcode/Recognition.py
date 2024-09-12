from datetime import datetime

import jpype
import base64
from io import BytesIO

from PIL import Image

from . import Assist

is_array = lambda var: isinstance(var, (list, tuple))
import os
import logging
from enum import Enum


class BarCodeReader(Assist.BaseJavaClass):
      """!
       BarCodeReader encapsulates an image which may contain one or several barcodes, it then can perform ReadBarCodes operation to detect barcodes.

       This sample shows how to detect Code39 and Code128 barcodes.
       \code
       reader = Recognition.BarCodeReader("test.png", None,  [DecodeType.CODE_39, DecodeType.CODE_128])
       for result in reader.readBarCodes():
             print("BarCode Type: " + result.getCodeTypeName())
             print("BarCode CodeText: " + result.getCodeText())
       \endcode
      """

      javaClassName = "com.aspose.mw.barcode.recognition.MwBarCodeReader"

      def __init__(self, image, areas, decodeTypes):
            """!
            Initializes a new instance of the BarCodeReader
            @param: image encoded as base64 string or path to image
            @param: areas array of object by type Rectangle
            @param: decodeTypes the array of objects by DecodeType
            """
            self.qualitySettings = None
            self.recognizedResults = None
            self.barcodeSettings = None
            try:
                  stringFormattedAreas = BarCodeReader.convertAreasToJavaFormattedAreas(areas)
                  decodeTypesArray = BarCodeReader.convertDecodeTypeToJavaDecodeType(decodeTypes)
                  base64Image = BarCodeReader.convertToBase64Image(image)

                  java_link = jpype.JClass(BarCodeReader.javaClassName)
                  javaClass = java_link(base64Image, stringFormattedAreas, decodeTypesArray)
                  super().__init__(javaClass)
                  self.init()
            except Exception as ex:
                  logging.error("Invalid arguments")
                  raise ex


      @staticmethod
      def convertDecodeTypeToJavaDecodeType(decodeTypes):
            if decodeTypes == None:
                  decodeTypes = DecodeType.ALL_SUPPORTED_TYPES
            if not is_array(decodeTypes):
                  decodeTypes = [decodeTypes]
            for decodeType in decodeTypes:
                  if not isinstance(decodeType.value, int):
                        raise Exception("Unsuported decodeType format")

            javaDecodeTypesArray = jpype.JArray(jpype.JInt)(len(decodeTypes))
            for i in range(len(javaDecodeTypesArray)):
                  javaDecodeTypesArray[i] = jpype.JInt(decodeTypes[i].value)

            return javaDecodeTypesArray

      @staticmethod
      def convertAreasToJavaFormattedAreas(areas):
            stringFormattedAreas = []
            if not areas == None:
                  stringFormattedAreas = []
                  if is_array(areas):
                        if not all(area is None for area in areas):
                              for area in areas:
                                    if (area == None) or (not (isinstance(area, Assist.Rectangle))):
                                          raise Exception('All elements of areas should be instances of Rectangle class')
                                    stringFormattedAreas.append(area.toString())
                  else:
                        if not isinstance(areas, Assist.Rectangle):
                              raise Exception('All elements of areas should be instances of Rectangle class')
                        stringFormattedAreas.append(areas.toString())

            javaAreasArray = jpype.JArray(jpype.JString)(len(stringFormattedAreas))
            for i in range(len(javaAreasArray)):
                  javaAreasArray[i] = jpype.JString(stringFormattedAreas[i])

            return javaAreasArray

      @staticmethod
      def construct(javaClass):
            barcodeReader = BarCodeReader(None, None, None)
            barcodeReader.setJavaClass(javaClass)
            return barcodeReader

      @staticmethod
      def convertToBase64Image(image):
            if image is None:
                  return None
            if isinstance(image, str):
                  if not os.path.exists(image):
                        raise Assist.BarCodeException("Path '" + image + "' is incorrect")
                  else:
                        image = Image.open(image)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue())

      def containsAny(self, decodeTypes):
            """!
            Determines whether any of the given decode types is included into
            @param: decodeTypes Types to verify.
            @return: bool Value is a true if any types are included into.
            """
            return self.getJavaClass().containsAny(BarCodeReader.convertDecodeTypeToJavaDecodeType(decodeTypes))

      def init(self):
            self.qualitySettings = QualitySettings(self.getJavaClass().getQualitySettings())
            self.barcodeSettings = BarcodeSettings(self.getJavaClass().getBarcodeSettings())

      def getTimeout(self):
            """!
            Gets the timeout of recognition process in milliseconds.
            \code
                 reader = Recognition.BarCodeReader("test.png", None, None)
                 reader.setTimeout(5000)
                 for result in reader.readBarCodes():
                    print("BarCode CodeText: " + result.getCodeText())
            \endcode
            @return: The timeout.
            """
            return self.getJavaClass().getTimeout()

      def setTimeout(self, value):
            """!
            Sets the timeout of recognition process in milliseconds.
            \code
                 reader = Recognition.BarCodeReader("test.png", None, None)
                 reader.setTimeout(5000)
                 results = reader.readBarCodes()
                 for result in results:
                     print("BarCode CodeText: " + result.getCodeText())
            \endcode
            @param: value The timeout.
            """
            self.getJavaClass().setTimeout(value)

      def abort(self):
            self.getJavaClass().abort()

      def getFoundBarCodes(self):
            """!
                Gets recognized BarCodeResult array

                This sample shows how to read barcodes with BarCodeReader
               \code
               reader = Recognition.BarCodeReader(image_path_code39, None,[Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
               reader.readBarCodes()
               for result in reader.getFoundBarCodes():
                  print("\nBarCode CodeText: " + result.getCodeText())
               \endcode
                @return: The recognized BarCodeResult array
            """
            return self.recognizedResults

      def getFoundCount(self):
            """!
                  Gets recognized barcodes count<hr><blockquote>
                  This sample shows how to read barcodes with BarCodeReader
                  \code
                     reader = Recognition.BarCodeReader(self.image_path, None,
                                       [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                     reader.readBarCodes()
                     print(f"\nFound {str(reader.getFoundCount())} barcodes")
                  \endcode
                  @return The recognized barcodes count
            """
            return self.getJavaClass().getFoundCount()

      def readBarCodes(self):
            """!
                 Reads BarCodeResult from the image.

                This sample shows how to read barcodes with BarCodeReader
                \code
                 reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                 for result in reader.readBarCodes():
                   print(f"\nBarCode CodeText: {result.getCodeText()}")
                 reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                 reader.readBarCodes()
                 for result in reader.getFoundBarCodes():
                   print(f"\nBarCode CodeText: {result.getCodeText()}")
                \endcode
                @return: Returns array of recognized {@code BarCodeResult}s on the image. If nothing is recognized, zero array is returned.
            """
            try:
                  self.recognizedResults = []
                  javaReadBarcodes = self.getJavaClass().readBarCodes()
                  i = 0
                  length = javaReadBarcodes.length
                  while (i < length):
                        self.recognizedResults.append(BarCodeResult(javaReadBarcodes[i]))
                        i += 1
                  return self.recognizedResults
            except Exception as e:
                  if "RecognitionAbortedException" in str(e):
                        raise RecognitionAbortedException(str(e), int(e.getExecutionTime()))
                  raise e

      def getQualitySettings(self):
            """!
                QualitySettings allows to configure recognition quality and speed manually.

                You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,

                HighQuality, MaxBarCodes or you can manually configure separate options.

                Default value of QualitySettings is NormalQuality.

                This sample shows how to use QualitySettings with BarCodeReader
                \code
                    reader = Recognition.BarCodeReader(self.image_path, None, None)
                    # set high performance mode
                    reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                    reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                    # normal quality mode is set by default
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                    reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                    # set high performance mode
                    reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
                    # set separate options
                    qualitySettings = reader.getQualitySettings()
                    qualitySettings.setAllowIncorrectBarcodes(True)
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                \endcode
                QualitySettings to configure recognition quality and speed.
            """
            return self.qualitySettings

      def setQualitySettings(self, value):
            """!
                QualitySettings allows to configure recognition quality and speed manually.

                 You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,

                 HighQuality, MaxBarCodes or you can manually configure separate options.

                 Default value of QualitySettings is NormalQuality.

                This sample shows how to use QualitySettings with BarCodeReader
                \code
                    reader = Recognition.BarCodeReader(self.image_path, None, None)
                    # set high performance mode
                    reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                    reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                    # normal quality mode is set by default
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                    reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                    # set high performance mode
                    reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
                    # set separate options
                    qualitySettings = reader.getQualitySettings()
                    qualitySettings.setAllowIncorrectBarcodes(True)
                    for result in reader.readBarCodes():
                        print(f"\nBarCode CodeText: {result.getCodeText()}")
                \endcode
                QualitySettings to configure recognition quality and speed.
            """
            self.getJavaClass().setQualitySettings(value.getJavaClass())

      def getBarcodeSettings(self):
            """!
                  The main BarCode decoding parameters. Contains parameters which make influence on recognized data.

                  return The main BarCode decoding parameters
            """
            return self.barcodeSettings

      def setBarCodeImage(self, imageResource, areas):
            """!
                Sets bitmap image and areas for Recognition.
                Must be called before ReadBarCodes() method.
                This sample shows how to detect Code39 and Code128 barcodes.
                \code
                    reader = Recognition.BarCodeReader(None, None, None)
                    reader.setBarCodeReadType([Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                    barcodeImage = Image.open(self.image_path)
                    width, height = barcodeImage.size
                    reader.setBarCodeImage(barcodeImage, [Assist.Rectangle(0, 0, width, height)])
                    results = reader.readBarCodes()
                    for result in results:
                        print(f"\nBarCode Type: {result.getCodeTypeName()}")
                        print(f"BarCode CodeText: {result.getCodeText()}")
                \endcode
                @param: imageResource path to image or object of PIL.Image
                @param: areas The areas list for recognition
                @throws BarCodeException
            """
            base64Image = BarCodeReader.convertToBase64Image(imageResource)
            stringFormattedAreas = BarCodeReader.convertAreasToJavaFormattedAreas(areas)
            self.getJavaClass().setBarCodeImage(base64Image, stringFormattedAreas)

      def setBarCodeReadType(self, types):
            """!
                 Sets SingleDecodeType type array for Recognition.

                 Must be called before readBarCodes() method.

                 This sample shows how to detect Code39 and Code128 barcodes.
                 \code
                   reader = Recognition.BarCodeReader(self.image_path, None, None)
                   reader.setBarCodeReadType([Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                   results = reader.readBarCodes()
                   for result in results:
                     print(f"\nBarCode Type: {result.getCodeTypeName()}")
                     print(f"BarCode CodeText: {result.getCodeText()}")
                 \endcode
                @param: types The SingleDecodeType type array to read.
            """
            types = BarCodeReader.convertDecodeTypeToJavaDecodeType(types)
            self.getJavaClass().setBarCodeReadType(types)

      def getBarCodeDecodeType(self):
            """!
                  Gets the decode type of the input barcode decoding
            """
            javaDecodeTypes = self.getJavaClass().getBarCodeDecodeType()
            barcodeTypesArray = []
            i = 0
            while (i < len(javaDecodeTypes)):
                  barcodeTypesArray.append(DecodeType(int(javaDecodeTypes[i])))
                  i += 1
            return barcodeTypesArray

      def exportToXml(self, xmlFile):
            """!
                 Exports BarCode properties to the xml-file specified
                 @param: xmlFile The name of  the file
                 @return: export completed successfully. Returns True in case of success and False otherwise
            """
            try:
                  xmlData = str(self.getJavaClass().exportToXml())
                  isSaved = xmlData != None
                  if isSaved:
                        text_file = open(xmlFile, "w")
                        text_file.write(xmlData)
                        text_file.close()
                  return isSaved
            except Exception as ex:
                  barcode_exception = Assist.BarCodeException(str(ex))
                  raise barcode_exception

      @staticmethod
      def importFromXml(xmlFile):
            """!
                  Exports BarCode properties to the xml-file specified
                  @param: xmlFile: xmlFile The name of  the file
                  @return: export completed successfully. Returns True in case of success and False otherwise
            """
            try:
                  with open(xmlFile, 'r') as file:
                        xmlData = file.read()
                        java_class_link = jpype.JClass(BarCodeReader.javaClassName)
                        return BarCodeReader.construct(java_class_link.importFromXml(xmlData[3:]))
            except Exception as ex:
                  barcode_exception = Assist.BarCodeException(ex)
                  raise barcode_exception

class Quadrangle(Assist.BaseJavaClass):
      """!
            Stores a set of four Points that represent a Quadrangle region.
      """
      javaClassName = "com.aspose.mw.barcode.recognition.MwQuadrangle"

      @staticmethod
      def EMPTY():
            """!
            Represents a Quadrangle structure with its properties left uninitialized.Value: Quadrangle
            """
            return Quadrangle(Assist.Point(0, 0), Assist.Point(0, 0), Assist.Point(0, 0), Assist.Point(0, 0))

      @staticmethod
      def construct(*args):
            quadrangle = Quadrangle.EMPTY()
            quadrangle.setJavaClass(args[0])
            return quadrangle

      def __init__(self, leftTop, rightTop, rightBottom, leftBottom):
            """!
                  Initializes a new instance of the Quadrangle structure with the describing points.
                  @param: leftTop A Point that represents the left-top corner of the Quadrangle.
                  @param: rightTop A Point that represents the right-top corner of the Quadrangle.
                  @param: rightBottom A Point that represents the right-bottom corner of the Quadrangle.
                  @param: leftBottom A Point that represents the left-bottom corner of the Quadrangle.
            """
            self.leftTop = leftTop
            self.rightTop = rightTop
            self.rightBottom = rightBottom
            self.leftBottom = leftBottom
            java_link = jpype.JClass(self.javaClassName)
            javaClass = java_link(leftTop.getJavaClass(), rightTop.getJavaClass(), rightBottom.getJavaClass(),
                                  leftBottom.getJavaClass())
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.leftTop = Assist.Point.construct(self.getJavaClass().getLeftTop())
            self.rightTop = Assist.Point.construct(self.getJavaClass().getRightTop())
            self.rightBottom = Assist.Point.construct(self.getJavaClass().getRightBottom())
            self.leftBottom = Assist.Point.construct(self.getJavaClass().getLeftBottom())

      def getLeftTop(self):
            """!
                  Gets left-top corner Point of Quadrangle regionValue: A left-top corner Point of Quadrangle region
            """
            return self.leftTop

      def setLeftTop(self, value):
            """!
                  Gets left-top corner Point of Quadrangle regionValue: A left-top corner Point of Quadrangle region
            """
            self.leftTop = value
            self.getJavaClass().setLeftTop(value.getJavaClass())

      def getRightTop(self):
            """!
                  Gets right-top corner Point of Quadrangle regionValue: A right-top corner Point of Quadrangle region
            """
            return self.rightTop

      def setRightTop(self, value):
            """!
                  Gets right-top corner Point of Quadrangle regionValue: A right-top corner Point of Quadrangle region
            """
            self.rightTop = value
            self.getJavaClass().setRightTop(value.getJavaClass())

      def getRightBottom(self):
            """!
                  Gets right-bottom corner Point of Quadrangle regionValue: A right-bottom corner Point of Quadrangle region
            """
            return self.rightBottom

      def setRightBottom(self, value):
            """!
                  Gets right-bottom corner Point of Quadrangle regionValue: A right-bottom corner Point of Quadrangle region
            """
            self.rightBottom = value
            self.getJavaClass().setRightBottom(value.getJavaClass())

      def getLeftBottom(self):
            """!
                  Gets left-bottom corner Point of Quadrangle regionValue: A left-bottom corner Point of Quadrangle region
            """
            return self.leftBottom

      def setLeftBottom(self, value):
            """!
                  Gets left-bottom corner Point of Quadrangle regionValue: A left-bottom corner Point of Quadrangle region
            """
            self.leftBottom = value
            self.getJavaClass().setLeftBottom(value.getJavaClass())

      def isEmpty(self):
            """!
            Tests whether all Points of this Quadrangle have values of zero.Value: Returns true if all Points of this Quadrangle have values of zero otherwise, false.
            """
            return self.getJavaClass().isEmpty()

      def contains(self, pt):
            """!
                 Determines if the specified Point is contained within this Quadrangle structure.
                 @param: pt The Point to test.
                 @return: Returns true if Point is contained within this Quadrangle structure otherwise, false.
            """
            return self.getJavaClass().contains(pt.getJavaClass())

      def containsPoint(self, x, y):
            """!
                 Determines if the specified point is contained within this Quadrangle structure.
                 @param: x The x point cordinate.
                 @param: y The y point cordinate.
                 @return: Returns true if point is contained within this Quadrangle structure otherwise, false.
            """
            return self.getJavaClass().contains(x, y)

      def containsQuadrangle(self, quad):
            """!
                 Determines if the specified Quadrangle is contained or intersect this Quadrangle structure.
                 @param: quad The Quadrangle to test.
                 @return: Returns true if Quadrangle is contained or intersect this Quadrangle structure otherwise, false.
            """
            return self.getJavaClass().contains(quad.getJavaClass())

      def containsRectangle(self, rect):
            """!
                 Determines if the specified Rectangle is contained or intersect this Quadrangle structure.
                 @param: rect The Rectangle to test.
                 @return: Returns true if Rectangle is contained or intersect this Quadrangle structure otherwise, false.
            """
            return self.getJavaClass().contains(rect)

      def equals(self, other):
            """!
                  Returns a value indicating whether this instance is equal to a specified Quadrangle value.
                  @param: other An Quadrangle value to compare to this instance.
                  @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(other.getJavaClass())

      def hashCode(self):
            """!
                  Returns the hash code for this instance.
                  @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
                  Returns a human-readable string representation of this Quadrangle.
                  @return: A string that represents this Quadrangle.
            """
            return self.getJavaClass().toString()

      def getBoundingRectangle(self):
            """!
                  Creates Rectangle bounding this Quadrangle
                  @return: returns Rectangle bounding this Quadrangle
            """
            return Assist.Rectangle.construct(self.getJavaClass().getBoundingRectangle())


class QRExtendedParameters(Assist.BaseJavaClass):
      """!
           Stores a QR Structured Append information of recognized barcode

           This sample shows how to get QR Structured Append data
           \code
               reader = Recognition.BarCodeReader(self.image_path_qr, None, Recognition.DecodeType.QR)
               for result in reader.readBarCodes():
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f"QR Structured Append Quantity: {str(result.getExtended().getQR().getQRStructuredAppendModeBarCodesQuantity())}")
                  print(f"QR Structured Append Index: {result.getExtended().getQR().getQRStructuredAppendModeBarCodeIndex()}")
                  print(f"QR Structured Append ParityData: {result.getExtended().getQR().getQRStructuredAppendModeParityData()}")
           \endcode
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            return
            # TODO: Implement init() method.

      def getQRStructuredAppendModeBarCodesQuantity(self):
            """!
            Gets the QR structured append mode barcodes quantity. Default value is -1.Value: The quantity of the QR structured append mode barcode.
            """
            return self.getJavaClass().getQRStructuredAppendModeBarCodesQuantity()

      def getQRStructuredAppendModeBarCodeIndex(self):
            """!
            Gets the index of the QR structured append mode barcode. Index starts from 0. Default value is -1.Value: The quantity of the QR structured append mode barcode.
            """
            return self.getJavaClass().getQRStructuredAppendModeBarCodeIndex()

      def getQRStructuredAppendModeParityData(self):
            """!
            Gets the QR structured append mode parity data. Default value is -1.Value: The index of the QR structured append mode barcode.
            """
            return self.getJavaClass().getQRStructuredAppendModeParityData()

      def isEmpty(self):
            """!
            Tests whether all parameters has only default values
            @return Returns {@code <b>true</b>} if all parameters has only default values; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().isEmpty()

      def equals(self, obj):
            """!
                 Returns a value indicating whether this instance is equal to a specified QRExtendedParameters value.
                 @param: obj An object value to compare to this instance.
                 @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this QRExtendedParameters.
            @return: A string that represents this QRExtendedParameters.
            """
            return self.getJavaClass().toString()


class Pdf417ExtendedParameters(Assist.BaseJavaClass):
      """!
            Stores a MacroPdf417 metadata information of recognized barcode

           This sample shows how to get Macro Pdf417 metadata
           \code
                    generator = Generation.BarcodeGenerator(Generation.EncodeTypes.MACRO_PDF_417, "12345")
                    generator.getParameters().getBarcode().getPdf417().setPdf417MacroFileID(10)
                    generator.getParameters().getBarcode().getPdf417().setPdf417MacroSegmentsCount(2)
                    generator.getParameters().getBarcode().getPdf417().setPdf417MacroSegmentID(1)
                    generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
                    reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.MACRO_PDF_417)
                    for result in reader.readBarCodes():
                        print("BarCode Type: " + result.getCodeTypeName())
                        print("BarCode CodeText: " + result.getCodeText())
                        print("Macro Pdf417 FileID: " + result.getExtended().getPdf417().getMacroPdf417FileID())
                        print("Macro Pdf417 Segments: " + str(result.getExtended().getPdf417().getMacroPdf417SegmentsCount()))
                        print("Macro Pdf417 SegmentID: " + str(result.getExtended().getPdf417().getMacroPdf417SegmentID()))           \endcode
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            return
            # TODO: Implement init() method.

      def getMacroPdf417FileID(self):
            """!
            Gets the file ID of the barcode, only available with MacroPdf417.Value: The file ID for MacroPdf417
            """
            return str(self.getJavaClass().getMacroPdf417FileID())

      def getMacroPdf417SegmentID(self):
            """!
            Gets the segment ID of the barcode,only available with MacroPdf417.Value: The segment ID of the barcode.
            """
            return int(self.getJavaClass().getMacroPdf417SegmentID())

      def getMacroPdf417SegmentsCount(self):
            """!
            Gets macro pdf417 barcode segments count. Default value is -1.Value: Segments count.
            """
            return int(self.getJavaClass().getMacroPdf417SegmentsCount())

      def getMacroPdf417FileName(self):
            """!
                 Macro PDF417 file name (optional).
                 @return: File name.
            """
            return self.getJavaClass().getMacroPdf417FileName()

      def getMacroPdf417FileSize(self):
            """!
            Macro PDF417 file size (optional).
            @return: File size.
            """
            return self.getJavaClass().getMacroPdf417FileSize()

      def getMacroPdf417Sender(self):
            """!
            Macro PDF417 sender name (optional).
            @return: Sender name
            """
            return self.getJavaClass().getMacroPdf417Sender()

      def getMacroPdf417Addressee(self):
            """!
            Macro PDF417 addressee name (optional).
            @return: Addressee name.
            """
            return self.getJavaClass().getMacroPdf417Addressee()

      def getMacroPdf417TimeStamp(self):
            """!
            Macro PDF417 time stamp (optional).
            @return: Time stamp.
            """
            return datetime.fromtimestamp(int(str(self.getJavaClass().getMacroPdf417TimeStamp())))

      def getMacroPdf417Checksum(self):
            """!
            Macro PDF417 checksum (optional).
            @return: Checksum.
            """
            return self.getJavaClass().getMacroPdf417Checksum()

      def isReaderInitialization(self):
            """!
            Used to instruct the reader to interpret the data contained within the symbol as programming for reader initialization.
            @return: Reader initialization flag
            """
            return self.getJavaClass().isReaderInitialization()

      def isLinked(self):
            """!
            Flag that indicates that the barcode must be linked to 1D barcode.
            @return Linkage flag
            """
            return self.getJavaClass().isLinked()

      def isCode128Emulation(self):
            """!
            Flag that indicates that the MicroPdf417 barcode encoded with 908, 909, 910 or 911 Code 128 emulation codewords.
            @return:  Code 128 emulation flag
            """
            return self.getJavaClass().isCode128Emulation()

      def getMacroPdf417Terminator(self):
            """!
            Indicates whether the segment is the last segment of a Macro PDF417 file.
            @return Terminator.
            """
            return self.getJavaClass().getMacroPdf417Terminator()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified Pdf417ExtendedParameters value.
            @param: obj An System.Object value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this Pdf417ExtendedParameters.
            @return: A string that represents this Pdf417ExtendedParameters.
            """
            return self.getJavaClass().toString()


class OneDExtendedParameters(Assist.BaseJavaClass):
      """!
          Stores special data of 1D recognized barcode like separate codetext and checksum

          This sample shows how to get 1D barcode value and checksum
          \code
                  generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
                  generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
                  reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.EAN_13)
                  for result in reader.readBarCodes():
                     print(f"\nBarCode Type: {result.getCodeTypeName()}")
                     print(f"BarCode CodeText: {result.getCodeText()}")
                     print(f"BarCode Value: {result.getExtended().getOneD().getValue()}")
                     print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
          \endcode
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            return
            # TODO: Implement init() method.

      def getValue(self):
            """!
            Gets the codetext of 1D barcodes without checksum. Value: The codetext of 1D barcodes without checksum.
            """
            return self.getJavaClass().getValue()

      def getCheckSum(self):
            """!
            Gets the checksum for 1D barcodes. Value: The checksum for 1D barcode.
            """
            return self.getJavaClass().getCheckSum()

      def isEmpty(self):
            """!
            Tests whether all parameters has only default values
            Value: Returns {@code <b>true</b>} if all parameters has only default values otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().isEmpty()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified OneDExtendedParameters value.
            @param: obj An System.Object value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this OneDExtendedParameters.
            @return: A string that represents this OneDExtendedParameters.
            """
            return self.getJavaClass().toString()


class Code128ExtendedParameters(Assist.BaseJavaClass):
      """!
            Stores special data of Code128 recognized barcode

            Represents the recognized barcode's region and barcode angle

           This sample shows how to get code128 raw values
           \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "12345")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.CODE_128)
              for result in reader.readBarCodes():
                  print("\nBarCode Type: " + result.getCodeTypeName())
                  print("BarCode CodeText: " + result.getCodeText())
                  print("Code128 Data Portions: " + str(result.getExtended().getCode128()))
            \endcode
      """

      def __init__(self, javaClass):
            self.code128DataPortions = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.code128DataPortions = Code128ExtendedParameters.convertCode128DataPortions(
                  self.getJavaClass().getCode128DataPortions())

      def convertCode128DataPortions(javaCode128DataPortions):
            code128DataPortions = []
            for i in range(len(javaCode128DataPortions)):
                  code128DataPortions.append(Code128DataPortion(javaCode128DataPortions[i]))
            return code128DataPortions

      def getCode128DataPortions(self):
            """!
            Gets Code128DataPortion array of recognized Code128 barcode Value of the Code128DataPortion.
            """
            return self.code128DataPortions

      def isEmpty(self):
            return self.getJavaClass().isEmpty()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified Code128ExtendedParameters value.
            @param: obj An System.Object value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this Code128ExtendedParameters.
            @return: A string that represents this Code128ExtendedParameters.
            """
            return self.getJavaClass().toString()

class BarCodeResult(Assist.BaseJavaClass):
      """!
      Stores recognized barcode data like SingleDecodeType type, {@code string} codetext,
      BarCodeRegionParameters region and other parameters
      This sample shows how to obtain BarCodeResult.
      \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "12345")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
              for result in reader.readBarCodes():
                  print("\nBarCode Type: " + result.getCodeTypeName())
                  print("BarCode CodeText: " + result.getCodeText())
                  print("BarCode Confidence: " + str(result.getConfidence()))
                  print("BarCode ReadingQuality: " + str(result.getReadingQuality()))
                  print("BarCode Angle: " + str(result.getRegion().getAngle()))
      \endcode
      """

      def __init__(self, javaClass):
            self.region = None
            self.extended = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.region = BarCodeRegionParameters(self.getJavaClass().getRegion())
            self.extended = BarCodeExtendedParameters(self.getJavaClass().getExtended())

      def getReadingQuality(self):
            """!
            Gets the reading quality. Works for 1D and postal barcodes. Value: The reading quality percent
            """
            return self.getJavaClass().getReadingQuality()

      def getConfidence(self):
            """!
            Gets recognition confidence level of the recognized barcode Value: BarCodeConfidence.

            Strong does not have fakes or misrecognitions, BarCodeConfidence.Moderate
            could sometimes have fakes or incorrect codetext because this confidence<br> level for barcodews with weak cheksum or even without it,

            BarCodeConfidence.NONE always has incorrect codetext and could be fake recognitions
            """
            return BarCodeConfidence(str(self.getJavaClass().getConfidence()))

      def getCodeText(self):
            """!
            Gets the code text Value: The code text of the barcode
            """
            return str(self.getJavaClass().getCodeText())

      def getCodeBytes(self):
            """!
            Gets the encoded code bytes Value: The code bytes of the barcode
            """
            _str = str(self.getJavaClass().getCodeBytes())
            return _str.split(",")

      def getCodeType(self):
            """!
            Gets the barcode type Value: The type information of the recognized barcode
            """
            return DecodeType(self.getJavaClass().getCodeType())

      def getCodeTypeName(self):
            """!
            Gets the name of the barcode type Value: The type name of the recognized barcode
            """
            return str(self.getJavaClass().getCodeTypeName())

      def getRegion(self):
            """!
            Gets the barcode region Value: The region of the recognized barcode
            """
            return self.region

      def getExtended(self):
            """!
            Gets extended parameters of recognized barcode Value: The extended parameters of recognized barcode
            """
            return self.extended

      def equals(self, other):
            """!
            Returns a value indicating whether this instance is equal to a specified BarCodeResult value.
            @param: other An BarCodeResult value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(other.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this BarCodeResult.
            @return: A string that represents this BarCodeResult.
            """
            return self.getJavaClass().toString()

      def deepClone(self):
            """!
             Creates a copy of BarCodeResult class.
             @return: Returns copy of BarCodeResult class.
            """
            return BarCodeResult(self)


class BarCodeRegionParameters(Assist.BaseJavaClass):
      """!
           Represents the recognized barcode's region and barcode angle
          This sample shows how to get barcode Angle and bounding quadrangle values
          \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "12345")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
              for result in reader.readBarCodes():
                  print("\nBarCode CodeText: " + result.getCodeText())
                  print("BarCode Angle: " + str(result.getRegion().getAngle()))
                  print("BarCode Quadrangle: " + str(result.getRegion().getQuadrangle()))
           \endcode
      """

      def __init__(self, javaClass):
            self.quad = None
            self.rect = None
            self.points = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self.quad = Quadrangle.construct(self.getJavaClass().getQuadrangle())
            self.rect = Assist.Rectangle.construct(self.getJavaClass().getRectangle())
            self.points = BarCodeRegionParameters.convertJavaPoints(self.getJavaClass().getPoints())
            # TODO: Implement init() method.

      def convertJavaPoints(javaPoints):
            points = []
            i = 0
            while (i < javaPoints.length):
                  points.append(Assist.Point(javaPoints[i].getX(), javaPoints[i].getY()))
                  i += 1

            return points

      def getQuadrangle(self):
            """!
            Gets Quadrangle bounding barcode region Value: Returns Quadrangle bounding barcode region
            """
            return self.quad

      def getAngle(self):
            """!
            Gets the angle of the barcode (0-360). Value: The angle for barcode (0-360).
            """
            return self.getJavaClass().getAngle()

      def getPoints(self):
            """!
            Gets Points array bounding barcode region Value: Returns Points array bounding barcode region
            """
            return self.points

      def getRectangle(self):
            """!
            Gets Rectangle bounding barcode region Value: Returns Rectangle bounding barcode region
            """
            return self.rect

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified BarCodeRegionParameters value.
            @param: obj An System.Object value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this BarCodeRegionParameters.
            @return: A string that represents this BarCodeRegionParameters.
            """
            return self.getJavaClass().toString()


class BarCodeExtendedParameters(Assist.BaseJavaClass):

      def __init__(self, javaClass):
            self._oneDParameters = None
            self._code128Parameters = None
            self._qrParameters = None
            self._pdf417Parameters = None
            self._dataBarParameters = None
            self._maxiCodeParameters = None
            self._dotCodeExtendedParameters = None
            self._dataMatrixExtendedParameters = None
            self._aztecExtendedParameters = None
            self._gs1CompositeBarExtendedParameters = None
            self._codabarExtendedParameters = None
            super().__init__(javaClass)
            self.init()

      def init(self):
            self._oneDParameters = OneDExtendedParameters(self.getJavaClass().getOneD())
            self._code128Parameters = Code128ExtendedParameters(self.getJavaClass().getCode128())
            self._qrParameters = QRExtendedParameters(self.getJavaClass().getQR())
            self._pdf417Parameters = Pdf417ExtendedParameters(self.getJavaClass().getPdf417())
            self._dataBarParameters = DataBarExtendedParameters(self.getJavaClass().getDataBar())
            self._maxiCodeParameters = MaxiCodeExtendedParameters(self.getJavaClass().getMaxiCode())
            self._dotCodeExtendedParameters = DotCodeExtendedParameters(self.getJavaClass().getDotCode())
            self._dataMatrixExtendedParameters = DataMatrixExtendedParameters(self.getJavaClass().getDataMatrix())
            self._aztecExtendedParameters = AztecExtendedParameters(self.getJavaClass().getAztec())
            self._gs1CompositeBarExtendedParameters = GS1CompositeBarExtendedParameters(self.getJavaClass().getGS1CompositeBar())
            self._codabarExtendedParameters = CodabarExtendedParameters(self.getJavaClass().getCodabar())

      def getDataBar(self):
            """!
            Gets a DataBar additional information DataBarExtendedParameters  of recognized barcode
            @return: mixed A DataBar additional information DataBarExtendedParameters of recognized barcode
            """
            return self._dataBarParameters

      def getMaxiCode(self):
            """!
            Gets a MaxiCode additional information MaxiCodeExtendedParameters  of recognized barcode
            @return: A MaxiCode additional information MaxiCodeExtendedParameters  of recognized barcode
            """
            return self._maxiCodeParameters

      def getOneD(self):
            """!
            Gets a special data OneDExtendedParameters of 1D recognized barcode Value: A special data OneDExtendedParameters of 1D recognized barcode
            """
            return self._oneDParameters

      def getDotCode(self):
            """!
             Gets a DotCode additional information{@code DotCodeExtendedParameters} of recognized barcodeValue: A DotCode additional information{@code DotCodeExtendedParameters} of recognized barcode
            """
            return self._dotCodeExtendedParameters

      def getDataMatrix(self):
            """!
            Gets a DotCode additional information{@code DotCodeExtendedParameters} of recognized barcode
            @return A DotCode additional information{@code DotCodeExtendedParameters} of recognized barcode
            """
            return self._dataMatrixExtendedParameters

      def getAztec(self):
            """
            Gets a Aztec additional information{@code AztecExtendedParameters} of recognized barcode
            @return A Aztec additional information{@code AztecExtendedParameters} of recognized barcode
            """
            return self._aztecExtendedParameters

      def getGS1CompositeBar(self):
            """!
            Gets a GS1CompositeBar additional information{@code GS1CompositeBarExtendedParameters} of recognized barcode
            @return A GS1CompositeBar additional information{@code GS1CompositeBarExtendedParameters} of recognized barcode
            """
            return self._gs1CompositeBarExtendedParameters

      def getCodabar(self):
            """!
            Gets a Codabar additional information{@code CodabarExtendedParameters} of recognized barcode
            @eturn: A Codabar additional information{@code CodabarExtendedParameters} of recognized barcode
            """
            return self._codabarExtendedParameters

      def getCode128(self):
            """!
            Gets a special data Code128ExtendedParameters of Code128 recognized barcode Value: A special data Code128ExtendedParameters of Code128 recognized barcode
            """
            return self._code128Parameters

      def getQR(self):
            """!
            Gets a QR Structured Append information QRExtendedParameters of recognized barcode Value: A QR Structured Append information QRExtendedParameters of recognized barcode
            """
            return self._qrParameters

      def getPdf417(self):
            """!
            Gets a MacroPdf417 metadata information Pdf417ExtendedParameters of recognized barcode Value: A MacroPdf417 metadata information Pdf417ExtendedParameters of recognized barcode
            """
            return self._pdf417Parameters

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified BarCodeExtendedParameters value.
            @param: obj An System.Object value to compare to this instance.
            @return: true if obj has the same value as this instance otherwise, false.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this BarCodeExtendedParameters.
            @return: A string that represents this BarCodeExtendedParameters.
            """
            return self.getJavaClass().toString()


class QualitySettings(Assist.BaseJavaClass):
      """!
           QualitySettings allows to configure recognition quality and speed manually.
           You can quickly set up QualitySettings by embedded presets: HighPerformance, NormalQuality,
           HighQuality, MaxBarCodes or you can manually configure separate options.
           Default value of QualitySettings is NormalQuality.
           This sample shows how to use QualitySettings with BarCodeReader
           \code
             reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
             # set high performance mode
              reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
              for result in reader.readBarCodes():
                  print("BarCode CodeText: " + result.getCodeText())
           \endcode
           \code
                  reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                  # normal quality mode is set by default
                  for result in reader.readBarCodes():
                      print("BarCode CodeText: " + result.getCodeText())
           \endcode
           \code
               reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
               # normal quality mode is set by default
               for result in reader.readBarCodes():
                 print("BarCode CodeText: " + result.getCodeText())
           \endcode
           \code
                  reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
                  # set max barcodes mode, which tries to find all possible barcodes, even incorrect. The slowest recognition mode
                  reader.setQualitySettings(Recognition.QualitySettings.getMaxQuality())
                  for result in reader.readBarCodes():
                      print("BarCode CodeText: " + result.getCodeText())
           \endcode
           \code
              reader = Recognition.BarCodeReader(self.image_path, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
              # set high performance mode
              reader.setQualitySettings(Recognition.QualitySettings.getHighPerformance())
              qualitySettings = reader.getQualitySettings()
              qualitySettings.setAllowIncorrectBarcodes(True)
              for result in reader.readBarCodes():
                  print("BarCode CodeText: " + result.getCodeText())
           \endcode
      """

      javaClassName = "com.aspose.mw.barcode.recognition.MwQualitySettings"

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      @staticmethod
      def initQualitySettings():
            javaClassName = "com.aspose.mw.barcode.recognition.MwQualitySettings"
            java_link = jpype.JClass(javaClassName)
            javaQualitySettings = java_link()
            return javaQualitySettings

      def init(self):
            pass

      @staticmethod
      def getHighPerformance():
            """!
            HighPerformance recognition quality preset. High quality barcodes are recognized well in this mode.
            \code
                 reader = Recognition.BarCodeReader("test.png")
                 reader.setQualitySettings(QualitySettings.getHighPerformance())
            \ebdcode
            @return HighPerformance recognition quality preset.
            """
            JavaQualitySettings = QualitySettings.initQualitySettings()
            return QualitySettings(JavaQualitySettings.getHighPerformance())

      @staticmethod
      def getNormalQuality():
            """!
            NormalQuality recognition quality preset. Suitable for most barcodes
            \code
              reader = Recognition.BarCodeReader(self.image_path_code128,None, [Recognition.DecodeType.CODE_128])
              reader.setQualitySettings(Recognition.QualitySettings.getNormalQuality())
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
            \endcode
            @return NormalQuality recognition quality preset.
            """
            JavaQualitySettings = QualitySettings.initQualitySettings()
            return QualitySettings(JavaQualitySettings.getNormalQuality())

      @staticmethod
      def getHighQuality():
            """!
            HighQuality recognition quality preset. This preset is developed for low quality barcodes.
             \code
                reader = Recognition.BarCodeReader(self.image_path_code128,None, [Recognition.DecodeType.CODE_128])
                reader.setQualitySettings(Recognition.QualitySettings.getHighQuality())
                results = reader.readBarCodes()
                for result in results:
                    print(f"\nBarCode Type: {result.getCodeTypeName()}")
                    print(f"BarCode CodeText: {result.getCodeText()}")
             \endcode
            """
            JavaQualitySettings = QualitySettings.initQualitySettings()
            return QualitySettings(JavaQualitySettings.getHighQuality())


      @staticmethod
      def getMaxQuality():
            """!
            MaxQuality recognition quality preset. This preset is developed to recognize all possible barcodes, even incorrect barcodes.
                                                                                                                            *  </p><p><hr><blockquote><pre>
            This sample shows how to use MaxQuality mode

            reader = Recognition.BarCodeReader(self.image_path_code128, None, [Recognition.DecodeType.CODE_128])
            # default mode is NormalQuality
            # set separate options
            reader.setQualitySettings(Recognition.QualitySettings.getMaxQuality())
            results = reader.readBarCodes()
            for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")

            @return: MaxQuality recognition quality preset.
            """
            JavaQualitySettings = QualitySettings.initQualitySettings()
            return QualitySettings(JavaQualitySettings.getMaxQuality())

      def getXDimension(self):
            """!
            Recognition mode which sets size (from 1 to infinity) of barcode minimal element: matrix cell or bar.
            @return: size (from 1 to infinity) of barcode minimal element: matrix cell or bar.
            """
            return XDimensionMode(self.getJavaClass().getXDimension())
      def setXDimension(self, value):
            """!
            Recognition mode which sets size (from 1 to infinity) of barcode minimal element: matrix cell or bar.
            """
            self.getJavaClass().setXDimension(value.value)

      def getMinimalXDimension(self):
            """!
            Minimal size of XDimension in pixels which is used with UseMinimalXDimension.
            @return:  Minimal size of XDimension in pixels which is used with UseMinimalXDimension.
            """
            return self.getJavaClass().getMinimalXDimension()

      def setMinimalXDimension(self, value):
            """!
             Minimal size of XDimension in pixels which is used with UseMinimalXDimension.
            :@param value:  Minimal size of XDimension in pixels which is used with UseMinimalXDimension.
            """
            self.getJavaClass().setMinimalXDimension(value)

      def getBarcodeQuality(self):
            """!
            Mode which enables methods to recognize barcode elements with the selected quality. Barcode element with lower quality requires more hard methods which slows the recognition.
            :@param self: Mode which enables methods to recognize barcode elements with the selected quality.
            """
            return BarcodeQualityMode(self.getJavaClass().getBarcodeQuality())

      def setBarcodeQuality(self, value):
            """!
            Mode which enables methods to recognize barcode elements with the selected quality. Barcode element with lower quality requires more hard methods which slows the recognition.
            :@param value: Mode which enables methods to recognize barcode elements with the selected quality.
            """
            self.getJavaClass().setBarcodeQuality(value.value)

      def getDeconvolution(self):
            """!
            Deconvolution (image restorations) mode which defines level of image degradation. Originally deconvolution is a function which can restore image degraded
            (convoluted) by any natural function like blur, during obtaining image by camera. Because we cannot detect image function which corrupt the image,
            we have to check most well know functions like sharp or mathematical morphology.
            @return: Deconvolution mode which defines level of image degradation.
            """
            return DeconvolutionMode(self.getJavaClass().getDeconvolution())

      def setDeconvolution(self, value):
            """!
            Deconvolution (image restorations) mode which defines level of image degradation. Originally deconvolution is a function which can restore image degraded
            (convoluted) by any natural function like blur, during obtaining image by camera. Because we cannot detect image function which corrupt the image,
            we have to check most well know functions like sharp or mathematical morphology.
            :@param value: Deconvolution mode which defines level of image degradation.
            """
            self.getJavaClass().setDeconvolution(value.value)

      def getInverseImage(self):
            """!
            Mode which enables or disables additional recognition of barcodes on images with inverted colors (luminance).
            @return: Additional recognition of barcodes on images with inverse colors
            """
            return InverseImageMode(self.getJavaClass().getInverseImage())

      def setInverseImage(self, value):
            """!
            Mode which enables or disables additional recognition of barcodes on images with inverted colors (luminance).
            :@param value: Additional recognition of barcodes on images with inverse colors
            """
            self.getJavaClass().setInverseImage(value.value)

      def getComplexBackground(self):
            """!
            Mode which enables or disables additional recognition of color barcodes on color images.
            :#return: Additional recognition of color barcodes on color images.
            """
            return ComplexBackgroundMode(self.getJavaClass().getComplexBackground())

      def setComplexBackground(self, value):
            """!
            Mode which enables or disables additional recognition of color barcodes on color images.
            :#param value: Additional recognition of color barcodes on color images.
            """
            self.getJavaClass().setComplexBackground(value.value)

      def getAllowIncorrectBarcodes(self):
            """!
            Allows engine to recognize barcodes which has incorrect checksumm or incorrect values. Mode can be used to recognize damaged barcodes with incorrect text.
            :#return: Allows engine to recognize incorrect barcodes.
            """
            return self.getJavaClass().getAllowIncorrectBarcodes()

      def setAllowIncorrectBarcodes(self, value):
            """!
            Allows engine to recognize barcodes which has incorrect checksumm or incorrect values. Mode can be used to recognize damaged barcodes with incorrect text.
            :@param value: Allows engine to recognize incorrect barcodes.
            """
            self.getJavaClass().setAllowIncorrectBarcodes(value)

class Code128DataPortion(Assist.BaseJavaClass):
      """!
            Contains the data of subtype for Code128 type barcode
      """
      javaClassName = "com.aspose.mw.barcode.recognition.MwCode128DataPortion"

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      def getData(self):
            """!
                  Gets the part of code text related to subtype.
                  @return: The part of code text related to subtype
            """
            return self.getJavaClass().getData()

      def getCode128SubType(self):
            """!
                 Gets the type of Code128 subset
                 @return: The type of Code128 subset
            """
            return Code128SubType(self.getJavaClass().getCode128SubType())

      def toString(self):
            """!
                 Returns a human-readable string representation of this {@code Code128DataPortion}.
                 @return: A string that represents this {@code Code128DataPortion}.
            """
            return self.getJavaClass().toString()


class DataBarExtendedParameters(Assist.BaseJavaClass):
      """!
          Stores a DataBar additional information of recognized barcode
          \code
         reader = Recognition.BarCodeReader(self.image_path_databar_omni, None,Recognition.DecodeType.DATABAR_OMNI_DIRECTIONAL)
         for result in reader.readBarCodes():
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
            print(f"QR Structured Append Quantity: "
                  f"{result.getExtended().getQR().getQRStructuredAppendModeBarCodesQuantity()}")
          \endcode
      """

      javaClassName = "com.aspose.mw.barcode.recognition.MwDataBarExtendedParameters"

      def init(self):
            pass

      def is2DCompositeComponent(self):
            """!
                Gets the DataBar 2D composite component flag. Default value is false.
                @return: The DataBar 2D composite component flag.
            """
            return self.getJavaClass().is2DCompositeComponent()

      def equals(self, obj):
            """!
                 Returns a value indicating whether this instance is equal to a specified DataBarExtendedParameters value.
                 @param: obj An System.Object value to compare to this instance.
                 @return: <b>true</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashcode(self):
            """!
                  Returns the hash code for this instance.
                  @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashcode()

      def toString(self):
            """!
                  Returns a human-readable string representation of this DataBarExtendedParameters"/>.
                  @return: A string that represents this DataBarExtendedParameters.
            """
            return self.getJavaClass().toString()

class AustraliaPostSettings(Assist.BaseJavaClass):
      """!
            AustraliaPost decoding parameters. Contains parameters which make influence on recognized data of AustraliaPost symbology.
      """

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            pass

      @staticmethod
      def construct(javaClass):
            australiaPostSettings = AustraliaPostSettings(None)
            australiaPostSettings.setJavaClass(javaClass)
            return australiaPostSettings

      def getCustomerInformationInterpretingType(self):
            """!
            Gets the Interpreting Type for the Customer Information of AustralianPost BarCode.DEFAULT is CustomerInformationInterpretingType.OTHER.
            @return: The interpreting type (CTable, NTable or Other) of customer information for AustralianPost BarCode
            """
            return CustomerInformationInterpretingType(self.getJavaClass().getCustomerInformationInterpretingType())

      def setCustomerInformationInterpretingType(self, value):
            """!
            Sets the Interpreting Type for the Customer Information of AustralianPost BarCode.DEFAULT is CustomerInformationInterpretingType.OTHER.
            @param: value: The interpreting type (CTable, NTable or Other) of customer information for AustralianPost BarCode
            """
            self.getJavaClass().setCustomerInformationInterpretingType(value.value)

      def getIgnoreEndingFillingPatternsForCTable(self):
            """!
            The flag which force AustraliaPost decoder to ignore last filling patterns in Customer Information Field during decoding as CTable method.
            CTable encoding method does not have any gaps in encoding table and sequence "333" of filling paterns is decoded as letter "z".
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "5912345678AB")
              generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
                  Generation.CustomerInformationInterpretingType.C_TABLE)
              pillow_image = generator.generateBarCodeImage()
              reader = Recognition.BarCodeReader(pillow_image, None, Recognition.DecodeType.AUSTRALIA_POST)
              reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(
                  Recognition.CustomerInformationInterpretingType.C_TABLE)
              reader.getBarcodeSettings().getAustraliaPost().setIgnoreEndingFillingPatternsForCTable(True)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
            \endcode

            @return: The flag which force AustraliaPost decoder to ignore last filling patterns during CTable method decoding
            """
            return self.getJavaClass().getIgnoreEndingFillingPatternsForCTable()

      def setIgnoreEndingFillingPatternsForCTable(self, value):
            self.getJavaClass().setIgnoreEndingFillingPatternsForCTable(value)

class BarcodeSettings(Assist.BaseJavaClass):

      def __init__(self, javaClass):
            super().__init__(javaClass)
            self.init()

      def init(self):
            self._australiaPost = AustraliaPostSettings(self.getJavaClass().getAustraliaPost())

      def getChecksumValidation(self):
            """!
            Enable checksum validation during recognition for 1D and Postal barcodes.
            Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
            Checksum never used: Codabar, PatchCode, Pharmacode, DataLogic2of5
            Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, ItalianPost25, Matrix2of5, MSI, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
            Checksum always used: Rest symbologies

            Example

            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None,Recognition.DecodeType.EAN_13)
              # checksum disabled
              reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.OFF)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f"BarCode Value: {result.getExtended().getOneD().getValue()}")
                  print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
            \endcode
            \code
            generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
            generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
            reader = Recognition.BarCodeReader(self.image_path_to_save, None,Recognition.DecodeType.EAN_13)
            # checksum enabled
            reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.ON)
            results = reader.readBarCodes()
            for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"BarCode Value: {result.getExtended().getOneD().getValue()}")
                print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
            \endcode
            @return:Enable checksum validation during recognition for 1D and Postal barcodes.
            """
            return ChecksumValidation(self.getJavaClass().getChecksumValidation())

      def setChecksumValidation(self, value):
            """!
            Enable checksum validation during recognition for 1D and Postal barcodes.
            Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
            Checksum never used: Codabar, PatchCode, Pharmacode, DataLogic2of5
            Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, ItalianPost25, Matrix2of5, MSI, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
            Checksum always used: Rest symbologies

            Example

            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None,Recognition.DecodeType.EAN_13)
              # checksum disabled
              reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.OFF)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
                  print(f"BarCode Value: {result.getExtended().getOneD().getValue()}")
                  print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
            \endcode
            \code
            generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
            generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
            reader = Recognition.BarCodeReader(self.image_path_to_save, None,Recognition.DecodeType.EAN_13)
            # checksum enabled
            reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.ON)
            results = reader.readBarCodes()
            for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
                print(f"BarCode Value: {result.getExtended().getOneD().getValue()}")
                print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
            \endcode
            @return:Enable checksum validation during recognition for 1D and Postal barcodes.
            """
            self.getJavaClass().setChecksumValidation(value.value)

      def getStripFNC(self):
            """!
            Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
            Example
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_CODE_128, "(02)04006664241007(37)1(400)7019590754")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save,None,Recognition.DecodeType.CODE_128)
              # StripFNC disabled
              reader.getBarcodeSettings().setStripFNC(False)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")

            \endcode
            \code
            reader = Recognition.BarCodeReader(self.image_path_to_save,None,Recognition.DecodeType.CODE_128)
            # StripFNC enabled
            reader.getBarcodeSettings().setStripFNC(False)
            results = reader.readBarCodes()
            for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
            \endcode
            @return: Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
            """
            return self.getJavaClass().getStripFNC()

      def setStripFNC(self, value):
             """!
            Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
            Example
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.GS_1_CODE_128, "(02)04006664241007(37)1(400)7019590754")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save,None,Recognition.DecodeType.CODE_128)
              # StripFNC disabled
              reader.getBarcodeSettings().setStripFNC(False)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")

            \endcode
            \code
            reader = Recognition.BarCodeReader(self.image_path_to_save,None,Recognition.DecodeType.CODE_128)
            # StripFNC enabled
            reader.getBarcodeSettings().setStripFNC(False)
            results = reader.readBarCodes()
            for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
            \endcode
            @return: Strip FNC1, FNC2, FNC3 characters from codetext. Default value is false.
            """
             self.getJavaClass().setStripFNC(value)

      def getDetectEncoding(self):
            """!
             The flag which force engine to detect codetext encoding for Unicode codesets. Default value is true.
             Example
             \code
             generator = BarcodeGenerator(EncodeTypes.QR, "Слово"))
             im = generator.generateBarcodeImage(BarcodeImageFormat.PNG)

             # detects encoding for Unicode codesets is enabled
             reader = Recognition.BarCodeReader(im, DecodeType.QR)
             reader.getBarcodeSettings().setDetectEncoding(true)
             for result in reader.readBarCodes():
                 print ("BarCode CodeText: " +result.getCodeText())

            \endcode
            \code
             # detect encoding is disabled
             reader = Recognition.BarCodeReader(im, DecodeType.QR)
             reader.getBarcodeSettings().setDetectEncoding(false)
             for result in reader.readBarCodes():
                 print ("BarCode CodeText: " +result.getCodeText())
            \endcode

            @return:The flag which force engine to detect codetext encoding for Unicode codesets
            """
            return self.getJavaClass().getDetectEncoding()

      def setDetectEncoding(self, value):
            """!
             The flag which force engine to detect codetext encoding for Unicode codesets. Default value is true.
             Example
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, "Слово")
              im = generator.generateBarCodeImage()
              # detects encoding for Unicode codesets is enabled
              reader = Recognition.BarCodeReader(im, None,Recognition.DecodeType.QR)
              reader.getBarcodeSettings().setDetectEncoding(True)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")

            \endcode
            \code
             # detect encoding is disabled
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, "Слово")
              im = generator.generateBarCodeImage()
              # detects encoding for Unicode codesets is enabled
              reader = Recognition.BarCodeReader(im, None,Recognition.DecodeType.QR)
              reader.getBarcodeSettings().setDetectEncoding(False)
              results = reader.readBarCodes()
              for result in results:
                  print(f"\nBarCode Type: {result.getCodeTypeName()}")
                  print(f"BarCode CodeText: {result.getCodeText()}")
            \endcode

            @param: value: The flag which force engine to detect codetext encoding for Unicode codesets
            """
            self.getJavaClass().setDetectEncoding(value)

      def getAustraliaPost(self):
            """!
            Gets AustraliaPost decoding parameters
            @return: The AustraliaPost decoding parameters which make influence on recognized data of AustraliaPost symbology
            """
            return self._australiaPost

class RecognitionAbortedException(Exception):

      javaClassName = "com.aspose.mw.barcode.recognition.MwRecognitionAbortedException"

      def getExecutionTime(self):
            """!
            Gets the execution time of current recognition session
            @return: The execution time of current recognition session
            """
            return self.javaClass.getExecutionTime()

      def setExecutionTime(self, value):
            """!
            Sets the execution time of current recognition session
            @param: value: value The execution time of current recognition session
            """
            self.javaClass.setExecutionTime(value)

      def __init__(self, message, executionTime):
            """!
            Initializes a new instance of the RecognitionAbortedException class with specified recognition abort message.

            @param: message: The error message of the exception.
            @param: executionTime: The execution time of current recognition session.
            """
            super().__init__(message)
            self.javaClass = None
            java_class_link = jpype.JClass(RecognitionAbortedException.javaClassName)
            if (message != None  and executionTime != None):
                  self.javaClass = java_class_link(message, executionTime)
            elif executionTime != None:
                  self.javaClass = java_class_link(executionTime)
            else:
                  self.javaClass = java_class_link()

      @staticmethod
      def construct(javaClass):
            exception = RecognitionAbortedException(None, None)
            exception.javaClass = javaClass
            return exception

      def init(self):
            pass


class MaxiCodeExtendedParameters(Assist.BaseJavaClass):
      """
      Stores a MaxiCode additional information of recognized barcode
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def getMaxiCodeMode(self):
            """!
            Gets a MaxiCode encode mode.
            Default value: Mode4
            """
            return self.getJavaClass().getMaxiCodeMode()

      def setMaxiCodeMode(self, maxiCodeMode):
            """!
            Sets a MaxiCode encode mode.
            Default value: Mode4
            """
            self.getJavaClass().setMaxiCodeMode(maxiCodeMode)

      def getMaxiCodeStructuredAppendModeBarcodeId(self):
            """!
            Gets a MaxiCode barcode id in structured append mode.
            Default value: 0
            """
            return self.getJavaClass().getMaxiCodeStructuredAppendModeBarcodeId()

      def setMaxiCodeStructuredAppendModeBarcodeId(self, value):
            """!
            Sets a MaxiCode barcode id in structured append mode.
            Default value: 0
            """
            self.getJavaClass().setMaxiCodeStructuredAppendModeBarcodeId(value)

      def getMaxiCodeStructuredAppendModeBarcodesCount(self):
            """!
            Gets a MaxiCode barcodes count in structured append mode.
            Default value: -1
            """
            return self.getJavaClass().getMaxiCodeStructuredAppendModeBarcodesCount()

      def setMaxiCodeStructuredAppendModeBarcodesCount(self, value):
            """!
            Sets a MaxiCode barcodes count in structured append mode.
            Default value: -1
            """
            self.getJavaClass().setMaxiCodeStructuredAppendModeBarcodesCount(value)

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified MaxiCodeExtendedParameters value.
            @param: obj:An System.Object value to compare to this instance
            @return:<b>true</b> if obj has the same value as this instance; otherwise, <b>false</b>.
            """
            return self.getJavaClass().equals(obj)

      def getHashCode(self):
            """!
            Returns a human-readable string representation of this MaxiCodeExtendedParameters.
            @return:A string that represents this MaxiCodeExtendedParameters.
            """
            return self.getJavaClass().getHashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this MaxiCodeExtendedParameters.
            @return:A string that represents this MaxiCodeExtendedParameters.
            """
            return self.getJavaClass().toString()

class DotCodeExtendedParameters(Assist.BaseJavaClass):
      """
      Stores special data of DotCode recognized barcode

      This sample shows how to get DotCode raw values
            \code
              generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DOT_CODE, "12345")
              generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
              reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.DOT_CODE)
              for result in reader.readBarCodes():
                  print("BarCode type: " + result.getCodeTypeName())
                  print("BarCode codetext: " + result.getCodeText())
                  print("DotCode barcode ID: " + str(result.getExtended().getDotCode().getDotCodeStructuredAppendModeBarcodeId()))
                  print("DotCode barcodes count: " + str(result.getExtended().getDotCode().getDotCodeStructuredAppendModeBarcodesCount()))
            \endcode
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def getDotCodeStructuredAppendModeBarcodesCount(self):
            """!
            Gets the DotCode structured append mode barcodes count. Default value is -1. Count must be a value from 1 to 35.
            @return: The count of the DotCode structured append mode barcode.
            """
            return self.getJavaClass().getDotCodeStructuredAppendModeBarcodesCount()

      def getDotCodeStructuredAppendModeBarcodeId(self):
            """!
            Gets the ID of the DotCode structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count. Default value is -1.
            @return: The ID of the DotCode structured append mode barcode.
            """
            return self.getJavaClass().getDotCodeStructuredAppendModeBarcodeId()

      def getDotCodeIsReaderInitialization(self):
            """!
            Indicates whether code is used for instruct reader to interpret the following data as instructions for initialization or reprogramming of the bar code reader.
            Default value is false.
            @param: self:
            @return:
            """
            return self.getJavaClass().getDotCodeIsReaderInitialization()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified {@code DotCodeExtendedParameters} value.
            @param: self:
            @param: obj: An System.Object value to compare to this instance.
            @return: {@code <b>true</b>} if obj has the same value as this instance; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @param: self:
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code DotCodeExtendedParameters}.
            @param: self:
            @return: A string that represents this {@code DotCodeExtendedParameters}.
            """
            return self.getJavaClass().toString()

      def init(self):
            pass


class DataMatrixExtendedParameters(Assist.BaseJavaClass):
      """!
      Stores special data of DataMatrix recognized barcode
      This sample shows how to get DataMatrix raw values
      \code
        generator = Generation.BarcodeGenerator(Generation.EncodeTypes.DATA_MATRIX, "12345")
        generator.save(self.image_path_to_save,  Generation.BarCodeImageFormat.PNG)
        reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.DATA_MATRIX)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
            print(f"DataMatrix barcode ID: {str(result.getExtended().getDataMatrix().getStructuredAppendBarcodeId())}")
            print(f"DataMatrix barcodes count: {str(result.getExtended().getDataMatrix().getStructuredAppendBarcodesCount())}")
            print(f"DataMatrix file ID:{str(result.getExtended().getDataMatrix().getStructuredAppendFileId())}")
            print(f"DataMatrix is reader programming: {result.getExtended().getDataMatrix().isReaderProgramming()}")
        \endcode
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def getStructuredAppendBarcodesCount(self):
            """!
            Gets the DataMatrix structured append mode barcodes count. Default value is -1. Count must be a value from 1 to 35.
            @return: The count of the DataMatrix structured append mode barcode.
            """
            return self.getJavaClass().getStructuredAppendBarcodesCount()

      def getStructuredAppendBarcodeId(self):
            """!
            Gets the ID of the DataMatrix structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count.
            Default value is -1.

            @return: The ID of the DataMatrix structured append mode barcode.
            """
            return self.getJavaClass().getStructuredAppendBarcodeId()

      def getStructuredAppendFileId(self):
            """
            Gets the ID of the DataMatrix structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count.
            Default value is -1.

            @return The ID of the DataMatrix structured append mode barcode.
            """
            return self.getJavaClass().getStructuredAppendFileId()

      def isReaderProgramming(self):
            """!
            Indicates whether code is used for instruct reader to interpret the following data as instructions for initialization or reprogramming of the bar code reader.
            Default value is false.
            """
            return self.getJavaClass().isReaderProgramming()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified {@code DataMatrixExtendedParameters} value.
            @param obj: An System.Object value to compare to this instance.
            @return {@code <b>true</b>} if obj has the same value as this instance; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code DataMatrixExtendedParameters}.
            @return: A string that represents this {@code DataMatrixExtendedParameters}.
            """
            return self.getJavaClass().toString()


class GS1CompositeBarExtendedParameters(Assist.BaseJavaClass):

      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def getOneDType(self):
            """!
            Gets the 1D (linear) barcode type of GS1 Composite
            @return 2D barcode type
            """
            return DecodeType(self.getJavaClass().getOneDType())

      def getOneDCodeText(self):
            """!
            Gets the 1D (linear) barcode value of GS1 Composite
            @return 1D barcode value
            """
            return self.getJavaClass().getOneDCodeText()

      def getTwoDType(self):
            """!
            Gets the 2D barcode type of GS1 Composite
            @return 2D barcode type
            """
            return DecodeType(self.getJavaClass().getTwoDType())

      def getTwoDCodeText(self):
            """!
            Gets the 2D barcode value of GS1 Composite
            @return 2D barcode value
            """
            return self.getJavaClass().getTwoDCodeText()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified {@code GS1CompositeBarExtendedParameters} value.
            @param obj: An System.Object value to compare to this instance.
            @return {@code <b>true</b>} if obj has the same value as this instance; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code GS1CompositeBarExtendedParameters}.
            @return  A string that represents this {@code GS1CompositeBarExtendedParameters}.
            """
            return self.getJavaClass().toString()

class AztecExtendedParameters(Assist.BaseJavaClass):
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def getStructuredAppendBarcodesCount(self):
            """!
            Gets the Aztec structured append mode barcodes count. Default value is 0. Count must be a value from 1 to 26.
            @return The barcodes count of the Aztec structured append mode.
            """
            return self.getJavaClass().getStructuredAppendBarcodesCount()

      def getStructuredAppendBarcodeId(self):
            """!
            Gets the ID of the Aztec structured append mode barcode. ID starts from 1 and must be less or equal to barcodes count. Default value is 0.
            @return The barcode ID of the Aztec structured append mode.
            """
            return self.getJavaClass().getStructuredAppendBarcodeId()

      def getStructuredAppendFileId(self):
            """!
            Gets the File ID of the Aztec structured append mode. Default value is empty string

            @return  The File ID of the Aztec structured append mode.
            """
            return self.getJavaClass().getStructuredAppendFileId()

      def isReaderInitialization(self):
            """!
            Indicates whether code is used for instruct reader to interpret the following data as instructions for initialization or reprogramming of the bar code reader.
            Default value is false.
            """
            return self.getJavaClass().isReaderInitialization()

      def equals(self, obj):
            """!
            Returns a value indicating whether this instance is equal to a specified {@code AztecExtendedParameters} value.
            @param obj: An System.Object value to compare to this instance.
            @return {@code <b>true</b>} if obj has the same value as this instance; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """!
            Returns the hash code for this instance.
            @return  A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """!
            Returns a human-readable string representation of this {@code AztecExtendedParameters}.
            @return  A string that represents this {@code AztecExtendedParameters}.
            """
            return self.getJavaClass().toString()

class CodabarExtendedParameters(Assist.BaseJavaClass):
      """!
      Stores a Codabar additional information of recognized barcode
      """
      def __init__(self, javaClass):
            super().__init__(javaClass)

      def init(self):
            pass

      def getCodabarStartSymbol(self):
            """
            Gets a Codabar start symbol.
            Default value: CodabarSymbol.A
            """
            return self.getJavaClass().getCodabarStartSymbol()

      def setCodabarStartSymbol(self, value):
            """
            Sets a Codabar start symbol.
            Default value: CodabarSymbol.A
            """
            self.getJavaClass().setCodabarStartSymbol(value)

      def getCodabarStopSymbol(self):
            """
            Gets a Codabar stop symbol.
            Default value: CodabarSymbol.A
            """
            return self.getJavaClass().getCodabarStopSymbol()

      def setCodabarStopSymbol(self, value):
            """!
            Gets or sets a Codabar stop symbol.
            Default value: CodabarSymbol.A
            """
            self.getJavaClass().setCodabarStopSymbol(value)

      def equals(self, obj):
            """
            Returns a value indicating whether this instance is equal to a specified {@code CodabarExtendedParameters} value.
            @param obj: obj An value to compare to this instance.
            @return: {@code <b>true</b>} if obj has the same value as this instance; otherwise, {@code <b>false</b>}.
            """
            return self.getJavaClass().equals(obj.getJavaClass())

      def hashCode(self):
            """
            Returns the hash code for this instance.
            @return: A 32-bit signed integer hash code.
            """
            return self.getJavaClass().hashCode()

      def toString(self):
            """
            Returns a human-readable string representation of this {@code CodabarExtendedParameters}.
            @return: A string that represents this {@code CodabarExtendedParameters}.
            """
            return self.getJavaClass().toString()


class DecodeType(Enum):
      """!
       Specify the type of barcode to read.
       This sample shows how to detect Code39 and Code128 barcodes.
       \code
          reader = Recognition.BarCodeReader(self.image_path_code39, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
          results = reader.readBarCodes()
          for result in results:
             print(f"\nBarCode Type: {result.getCodeTypeName()}")
             print(f"BarCode CodeText: {result.getCodeText()}")
        \endcode
      """

      ## Unspecified decode type.
      NONE = -1

      ##  Specifies that the data should be decoded with {@code <b>CODABAR</b>} barcode specification
      CODABAR = 0

      ## Specifies that the data should be decoded with {@code <b>CODE 11</b>} barcode specification
      CODE_11 = 1

      ## Specifies that the data should be decoded with {@code <b>Code 39</b>} basic charset barcode specification: ISO/IEC 16388
      CODE_39 = 2

      ## Specifies that the data should be decoded with {@code <b>Code 39</b>} full ASCII charset barcode specification: ISO/IEC 16388
      CODE_39_FULL_ASCII = 3

      ## Specifies that the data should be decoded with {@code <b>CODE 93</b>} barcode specification
      CODE_93 = 5

      ##  Specifies that the data should be decoded with {@code <b>CODE 128</b>} barcode specification
      CODE_128 = 6

      ## Specifies that the data should be decoded with {@code <b>GS1 CODE 128</b>} barcode specification
      GS_1_CODE_128 = 7

      ## Specifies that the data should be decoded with {@code <b>EAN-8</b>} barcode specification
      EAN_8 = 8

      ##  Specifies that the data should be decoded with {@code <b>EAN-13</b>} barcode specification
      EAN_13 = 9

      ##  Specifies that the data should be decoded with {@code <b>EAN14</b>} barcode specification
      EAN_14 = 10

      ##  Specifies that the data should be decoded with {@code <b>SCC14</b>} barcode specification
      SCC_14 = 11

      ##  Specifies that the data should be decoded with {@code <b>SSCC18</b>} barcode specification
      SSCC_18 = 12

      ## Specifies that the data should be decoded with {@code <b>UPC-A</b>} barcode specification
      UPCA = 13

      ##  Specifies that the data should be decoded with {@code <b>UPC-E</b>} barcode specification
      UPCE = 14

      ## Specifies that the data should be decoded with {@code <b>ISBN</b>} barcode specification
      ISBN = 15

      ##  Specifies that the data should be decoded with {@code <b>Standard 2 of 5</b>} barcode specification
      STANDARD_2_OF_5 = 16

      ##  Specifies that the data should be decoded with {@code <b>INTERLEAVED 2 of 5</b>} barcode specification
      INTERLEAVED_2_OF_5 = 17

      ##  Specifies that the data should be decoded with {@code <b>Matrix 2 of 5</b>} barcode specification
      MATRIX_2_OF_5 = 18

      ##  Specifies that the data should be decoded with {@code <b>Italian Post 25</b>} barcode specification
      ITALIAN_POST_25 = 19

      ##  Specifies that the data should be decoded with {@code <b>IATA 2 of 5</b>} barcode specification. IATA (International Air Transport Association) uses this barcode for the management of air cargo.
      IATA_2_OF_5 = 20

      ##  Specifies that the data should be decoded with {@code <b>ITF14</b>} barcode specification
      ITF_14 = 21

      ## Specifies that the data should be decoded with {@code <b>ITF6</b>} barcode specification
      ITF_6 = 22

      ## Specifies that the data should be decoded with {@code <b>MSI Plessey</b>} barcode specification
      MSI = 23

      ## Specifies that the data should be decoded with {@code <b>VIN</b>} (Vehicle Identification Number) barcode specification
      VIN = 24

      ##  Specifies that the data should be decoded with {@code <b>DeutschePost Ident code</b>} barcode specification
      DEUTSCHE_POST_IDENTCODE = 25

      ##  Specifies that the data should be decoded with {@code <b>DeutschePost Leit code</b>} barcode specification
      DEUTSCHE_POST_LEITCODE = 26

      ##  Specifies that the data should be decoded with {@code <b>OPC</b>} barcode specification
      OPC = 27

      ##  Specifies that the data should be decoded with {@code <b>PZN</b>} barcode specification. This symbology is also known as Pharma Zentral Nummer
      PZN = 28

      ##  Specifies that the data should be decoded with {@code <b>Pharmacode</b>} barcode. This symbology is also known as Pharmaceutical BINARY Code
      PHARMACODE = 29

      ##   Specifies that the data should be decoded with {@code <b>DataMatrix</b>} barcode symbology
      DATA_MATRIX = 30

      ## Specifies that the data should be decoded with {@code <b>GS1DataMatrix</b>} barcode symbology
      GS_1_DATA_MATRIX = 31

      ##  Specifies that the data should be decoded with {@code <b>QR Code</b>} barcode specification
      QR = 32

      ##  Specifies that the data should be decoded with {@code <b>Aztec</b>} barcode specification
      AZTEC = 33

      ## Specifies that the data should be decoded with {@code <b>GS1 Aztec</b>} barcode specification
      GS_1_AZTEC = 81

      ##  Specifies that the data should be decoded with {@code <b>Pdf417</b>} barcode symbology
      PDF_417 = 34

      ## Specifies that the data should be decoded with {@code <b>MacroPdf417</b>} barcode specification
      MACRO_PDF_417 = 35

      ## Specifies that the data should be decoded with {@code <b>MicroPdf417</b>} barcode specification
      MICRO_PDF_417 = 36

      ## Specifies that the data should be decoded with <b>MicroPdf417</b> barcode specification
      GS_1_MICRO_PDF_417 = 82

      ##  Specifies that the data should be decoded with {@code <b>CodablockF</b>} barcode specification
      CODABLOCK_F = 65

      ##  Specifies that the data should be decoded with <b>Royal Mail Mailmark</b> barcode specification.
      MAILMARK = 66

      ##  Specifies that the data should be decoded with {@code <b>Australia Post</b>} barcode specification
      AUSTRALIA_POST = 37

      ##  Specifies that the data should be decoded with {@code <b>Postnet</b>} barcode specification
      POSTNET = 38

      ##  Specifies that the data should be decoded with {@code <b>Planet</b>} barcode specification
      PLANET = 39

      ##  Specifies that the data should be decoded with USPS {@code <b>OneCode</b>} barcode specification
      ONE_CODE = 40

      ##  Specifies that the data should be decoded with {@code <b>RM4SCC</b>} barcode specification. RM4SCC (Royal Mail 4-state Customer Code) is used for automated mail sort process in UK.
      RM_4_SCC = 41

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR omni-directional</b>} barcode specification
      DATABAR_OMNI_DIRECTIONAL = 42

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR truncated</b>} barcode specification
      DATABAR_TRUNCATED = 43

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR limited</b>} barcode specification
      DATABAR_LIMITED = 44

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR expanded</b>} barcode specification
      DATABAR_EXPANDED = 45

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR stacked omni-directional</b>} barcode specification
      DATABAR_STACKED_OMNI_DIRECTIONAL = 53

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR stacked</b>} barcode specification
      DATABAR_STACKED = 54

      ##  Specifies that the data should be decoded with {@code <b>GS1 DATABAR expanded stacked</b>} barcode specification
      DATABAR_EXPANDED_STACKED = 55

      ##  Specifies that the data should be decoded with {@code <b>Patch code</b>} barcode specification. Barcode symbology is used for automated scanning
      PATCH_CODE = 46

      ##  Specifies that the data should be decoded with {@code <b>ISSN</b>} barcode specification
      ISSN = 47

      ##  Specifies that the data should be decoded with {@code <b>ISMN</b>} barcode specification
      ISMN = 48

      ##  Specifies that the data should be decoded with {@code <b>Supplement(EAN2 EAN5)</b>} barcode specification
      SUPPLEMENT = 49

      ##  Specifies that the data should be decoded with {@code <b>Australian Post Domestic eParcel Barcode</b>} barcode specification
      AUSTRALIAN_POSTE_PARCEL = 50

      ##  Specifies that the data should be decoded with {@code <b>Swiss Post Parcel Barcode</b>} barcode specification
      SWISS_POST_PARCEL = 51

      ##   Specifies that the data should be decoded with {@code <b>SCode16K</b>} barcode specification
      CODE_16_K = 52

      ##  Specifies that the data should be decoded with {@code <b>MicroQR Code</b>} barcode specification
      MICRO_QR = 56

      ## Specifies that the data should be decoded with <b>RectMicroQR (rMQR) Code</b> barcode specification
      RECT_MICRO_QR = 83

      ##  Specifies that the data should be decoded with {@code <b>CompactPdf417</b>} (Pdf417Truncated) barcode specification
      COMPACT_PDF_417 = 57

      ##  Specifies that the data should be decoded with {@code <b>GS1 QR</b>} barcode specification
      GS_1_QR = 58

      ##  Specifies that the data should be decoded with {@code <b>MaxiCode</b>} barcode specification
      MAXI_CODE = 59

      ##  Specifies that the data should be decoded with {@code <b>MICR E-13B</b>} blank specification
      MICR_E_13_B = 60

      ##  Specifies that the data should be decoded with {@code <b>Code32</b>} blank specification
      CODE_32 = 61

      ##  Specifies that the data should be decoded with {@code <b>DataLogic 2 of 5</b>} blank specification
      DATA_LOGIC_2_OF_5 = 62

      ##  Specifies that the data should be decoded with {@code <b>DotCode</b>} blank specification
      DOT_CODE = 63

      ## Specifies that the data should be decoded with {@code <b>GS1 DotCode</b>} blank specification
      GS_1_DOT_CODE = 77

      ##  Specifies that the data should be decoded with {@code <b>DotCode</b>} blank specification
      DUTCH_KIX = 64

      ## Specifies that the data should be decoded with {@code <b>HIBC LIC Code39</b>} blank specification
      HIBC_CODE_39_LIC = 67

      ## Specifies that the data should be decoded with {@code <b>HIBC LIC Code128</b>} blank specification
      HIBC_CODE_128_LIC = 68

      ## Specifies that the data should be decoded with {@code <b>HIBC LIC Aztec</b>} blank specification
      HIBC_AZTEC_LIC = 69

      ## Specifies that the data should be decoded with {@code <b>HIBC LIC DataMatrix</b>} blank specification
      HIBC_DATA_MATRIX_LIC = 70

      ## Specifies that the data should be decoded with {@code <b>HIBC LIC QR</b>} blank specification
      HIBCQRLIC = 71

      ## Specifies that the data should be decoded with {@code <b>HIBC PAS Code39</b>} blank specification
      HIBC_CODE_39_PAS = 72

      ## Specifies that the data should be decoded with {@code <b>HIBC PAS Code128</b>} blank specification
      HIBC_CODE_128_PAS = 73

      ## Specifies that the data should be decoded with {@code <b>HIBC PAS Aztec</b>} blank specification
      HIBC_AZTEC_PAS = 74

      ## Specifies that the data should be decoded with {@code <b>HIBC PAS DataMatrix</b>} blank specification
      HIBC_DATA_MATRIX_PAS = 75

      ## Specifies that the data should be decoded with {@code <b>HIBC PAS QR</b>} blank specification
      HIBCQRPAS = 76

      ## Specifies that the data should be decoded with <b>Han Xin Code</b> blank specification
      HAN_XIN = 78

      ## Specifies that the data should be decoded with <b>Han Xin Code</b> blank specification
      GS_1_HAN_XIN = 79

      ## Specifies that the data should be decoded with {@code <b>GS1 Composite Bar</b>} barcode specification
      GS_1_COMPOSITE_BAR = 80

      ## Specifies that data will be checked with all of  1D  barcode symbologies
      TYPES_1D = 97

      ## Specifies that data will be checked with all of  1.5D POSTAL  barcode symbologies, like  Planet, Postnet, AustraliaPost, OneCode, RM4SCC, DutchKIX
      POSTAL_TYPES = 95

      ## Specifies that data will be checked with most commonly used symbologies
      MOST_COMMON_TYPES = 96

      ## Specifies that data will be checked with all of <b>2D</b> barcode symbologies
      TYPES_2D = 98

      ## Specifies that data will be checked with all available symbologies
      ALL_SUPPORTED_TYPES = 99

      javaClassName = "com.aspose.mw.barcode.recognition.MwDecodeTypeUtils"

      @staticmethod
      def is1D(symbology):
            """!
            Determines if the specified BaseDecodeType contains any 1D barcode symbology
            @param: symbology
            @return: string <b>true</b> if BaseDecodeType contains any 1D barcode symbology; otherwise, returns <b>false</b>.
            """
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.is1D(symbology)

      @staticmethod
      def isPostal(symbology):
            """!
            Determines if the specified BaseDecodeType contains any Postal barcode symbology
            @param: symbology symbology The BaseDecodeType to test
            @return: Returns <b>true</b> if BaseDecodeType contains any Postal barcode symbology; otherwise, returns <b>false</b>.
            """
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.isPostal(symbology)

      @staticmethod
      def is2D(symbology):
            """!
            Determines if the specified BaseDecodeType contains any 2D barcode symbology
            @param: symbology symbology The BaseDecodeType to test.
            @return: Returns <b>True</b> if BaseDecodeType contains any 2D barcode symbology; otherwise, returns <b>False</b>.
            """
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.is2D(symbology)

      @staticmethod
      def containsAny(decodeType, decodeTypes):
            java_link = jpype.JClass(DecodeType.javaClassName)
            javaClass = java_link()
            return javaClass.containsAny(decodeTypes)


class Code128SubType(Enum):

      ## ASCII characters 00 to 95 (0–9, A–Z and control codes), special characters, and FNC 1–4
      CODE_SET_A = 1

      ##  ASCII characters 32 to 127 (0–9, A–Z, a–z), special characters, and FNC 1–4
      CODE_SET_B = 2

      ##    00–99 (encodes two digits with a single code point) and FNC1
      CODE_SET_C = 3


class CustomerInformationInterpretingType(Enum):
      """!
       Defines the interpreting type(C_TABLE or N_TABLE) of customer information for AustralianPost BarCode.
      """
       ##
       # Use C_TABLE to interpret the customer information. Allows A..Z, a..z, 1..9, space and   sing.
       # \code
       #   generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "5912345678ABCde")
       #   generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(Generation.CustomerInformationInterpretingType.C_TABLE)
       #   image = generator.generateBarCodeImage()
       #   reader = Recognition.BarCodeReader(image, None,Recognition.DecodeType.AUSTRALIA_POST)
       #   reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(Recognition.CustomerInformationInterpretingType.C_TABLE)
       #   results = reader.readBarCodes()
       #   for result in results:
       #       print(f"\nBarCode Type: {result.getCodeTypeName()}")
       #       print(f"BarCode CodeText: {result.getCodeText()}")
       # \endcode
      C_TABLE = 0
        ##
        # Use N_TABLE to interpret the customer information. Allows digits.
       # \code
       #  generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "59123456781234567")
       #  generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
       #      Generation.CustomerInformationInterpretingType.N_TABLE)
       #  image = generator.generateBarCodeImage()
       #  reader = Recognition.BarCodeReader(image, None,Recognition.DecodeType.AUSTRALIA_POST)
       #  reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(Recognition.CustomerInformationInterpretingType.N_TABLE)
       #  for result in reader.readBarCodes():
       #      print("BarCode Type: " + result.getCodeType())
       #      print("BarCode CodeText: " + result.getCodeText())
       # \endcode
      N_TABLE = 1
       ##
       # Do not interpret the customer information. Allows 0, 1, 2 or 3 symbol only.
       # \code
       #  generator = Generation.BarcodeGenerator(Generation.EncodeTypes.AUSTRALIA_POST, "59123456781234567")
       #  generator.getParameters().getBarcode().getAustralianPost().setAustralianPostEncodingTable(
       #      Generation.CustomerInformationInterpretingType.N_TABLE)
       #  image = generator.generateBarCodeImage()
       #  reader = Recognition.BarCodeReader(image, None, Recognition.DecodeType.AUSTRALIA_POST)
       #  reader.getBarcodeSettings().getAustraliaPost().setCustomerInformationInterpretingType(
       #      Recognition.CustomerInformationInterpretingType.OTHER)
       #  results = reader.readBarCodes()
       #  for result in results:
       #      print(f"\nBarCode Type: {result.getCodeTypeName()}")
       #      print(f"BarCode CodeText: {result.getCodeText()}")
       # \endcode
      OTHER = 2

class BarCodeConfidence(Enum):
      """!
       Contains recognition confidence level

       This sample shows how BarCodeConfidence changed, depending on barcode type
       \code
          #Moderate confidence
          generator = Generation.BarcodeGenerator(Generation.EncodeTypes.CODE_128, "12345")
          generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
          reader = Recognition.BarCodeReader(self.image_path_to_save, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.CODE_128])
          for result in reader.readBarCodes():
              print("\nBarCode Type: " + result.getCodeTypeName())
              print("BarCode CodeText: " + result.getCodeText())
              print("BarCode Confidence: " + str(result.getConfidence()))
              print("BarCode ReadingQuality: " + str(result.getReadingQuality()))
          #Strong confidence
          generator = Generation.BarcodeGenerator(Generation.EncodeTypes.QR, "12345")
          generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
          reader = Recognition.BarCodeReader(self.image_path_to_save, None, [Recognition.DecodeType.CODE_39, Recognition.DecodeType.QR])
          for result in reader.readBarCodes():
            print("\nBarCode Type: " + result.getCodeTypeName())
            print("BarCode CodeText: " + result.getCodeText())
            print("BarCode Confidence: " + str(result.getConfidence()))
            print("BarCode ReadingQuality: " + str(result.getReadingQuality()))
       \endcode
      """
      ## Recognition confidence of barcode where codetext was not recognized correctly or barcode was detected as posible fake
      NONE = "0"

      ## Recognition confidence of barcode (mostly 1D barcodes) with weak checksumm or even without it. Could contains some misrecognitions in codetext
      # or even fake recognitions if  is low
      # @see BarCodeResult.getReadingQuality()
      MODERATE = "80"

      ## Recognition confidence which was confirmed with BCH codes like Reed–Solomon. There must not be errors in read codetext or fake recognitions
      STRONG = "100"


class ChecksumValidation(Enum):
      """!
      Enable checksum validation during recognition for 1D barcodes.
      Default is treated as Yes for symbologies which must contain checksum, as No where checksum only possible.
      Checksum never used: Codabar
      Checksum is possible: Code39 Standard/Extended, Standard2of5, Interleaved2of5, Matrix2of5, ItalianPost25, DeutschePostIdentcode, DeutschePostLeitcode, VIN
      Checksum always used: Rest symbologies
      This sample shows influence of ChecksumValidation on recognition quality and results
      \code
        generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
        generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
        reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.EAN_13)
        # checksum disabled
        reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.OFF)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
            print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
      \endcode
      \code
        generator = Generation.BarcodeGenerator(Generation.EncodeTypes.EAN_13, "1234567890128")
        generator.save(self.image_path_to_save, Generation.BarCodeImageFormat.PNG)
        reader = Recognition.BarCodeReader(self.image_path_to_save, None, Recognition.DecodeType.EAN_13)
        # checksum enabled
        reader.getBarcodeSettings().setChecksumValidation(Recognition.ChecksumValidation.ON)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
            print(f"BarCode Checksum: {result.getExtended().getOneD().getCheckSum()}")
     \endcode
      """

      ## If checksum is required by the specification - it will be validated.
      DEFAULT = 0

      ## Always validate checksum if possible.
      ON = 1

      ## Do not validate checksum.
      OFF = 2

class DeconvolutionMode(Enum):
      """!
      Deconvolution (image restorations) mode which defines level of image degradation. Originally deconvolution is a function which can restore image degraded
      (convoluted) by any natural function like blur, during obtaining image by camera. Because we cannot detect image function which corrupt the image,
      we have to check most well know functions like sharp or mathematical morphology.
      This sample shows how to use Deconvolution mode
      \code
        reader = Recognition.BarCodeReader(self.image_path_code39, None,[Recognition.DecodeType.CODE_39_FULL_ASCII, Recognition.DecodeType.CODE_128])
        reader.getQualitySettings().setDeconvolution(Recognition.DeconvolutionMode.SLOW)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
      \endcode
      """

      ##Enables fast deconvolution methods for high quality images.
      FAST = 0
      ##Enables normal deconvolution methods for common images.
      NORMAL = 1
      ##Enables slow deconvolution methods for low quality images.
      SLOW = 2

class InverseImageMode(Enum):
      """!
      Mode which enables or disables additional recognition of barcodes on images with inverted colors (luminance).
      \code
        reader = Recognition.BarCodeReader(self.image_path_code39, None,[Recognition.DecodeType.CODE_39_FULL_ASCII, Recognition.DecodeType.CODE_128])
        reader.getQualitySettings().setInverseImage(Recognition.InverseImageMode.ENABLED)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
      \endcode
      """

      ## At this time the same as Disabled. Disables additional recognition of barcodes on inverse images.</p>
      AUTO = 0

      ## Disables additional recognition of barcodes on inverse images.</p>
      DISABLED = 1

      ## Enables additional recognition of barcodes on inverse images</p>
      ENABLED = 2

class XDimensionMode(Enum):
      """!
      Recognition mode which sets size (from 1 to infinity) of barcode minimal element: matrix cell or bar.

      This sample shows how to use XDimension mode
      \code
            reader = Recognition.BarCodeReader(self.image_path_code39, None,[Recognition.DecodeType.CODE_39_FULL_ASCII, Recognition.DecodeType.CODE_128])
            reader.getQualitySettings().setXDimension(Recognition.XDimensionMode.SMALL)
            results = reader.readBarCodes()
            for result in results:
                print(f"\nBarCode Type: {result.getCodeTypeName()}")
                print(f"BarCode CodeText: {result.getCodeText()}")
      \endcode
      """
      ## Value of XDimension is detected by AI (SVM). At this time the same as Normal</p>
      AUTO = 0

      ## Detects barcodes with small XDimension in 1 pixel or more with quality from BarcodeQuality</p>
      SMALL = 1

      ## Detects barcodes with classic XDimension in 2 pixels or more with quality from BarcodeQuality or high quality barcodes.</p>
      NORMAL = 2

      ## Detects barcodes with large XDimension with quality from BarcodeQuality captured with high-resolution cameras.</p>
      LARGE = 3

      ## Detects barcodes from size set in MinimalXDimension with quality from BarcodeQuality</p>
      USE_MINIMAL_X_DIMENSION = 4

class ComplexBackgroundMode(Enum):
      """!
      Mode which enables or disables additional recognition of color barcodes on color images.
      \code
          reader = Recognition.BarCodeReader(self.image_path_code39, None,[Recognition.DecodeType.CODE_39_FULL_ASCII, Recognition.DecodeType.CODE_128])
          reader.getQualitySettings().setComplexBackground(Recognition.ComplexBackgroundMode.ENABLED)
          results = reader.readBarCodes()
          for result in results:
             print(f"\nBarCode Type: {result.getCodeTypeName()}")
             print(f"BarCode CodeText: {result.getCodeText()}")
      \endcode
      """
      ## At this time the same as Disabled. Disables additional recognition of color barcodes on color images.</p>
      AUTO = 0
      ## Disables additional recognition of color barcodes on color images.</p>
      DISABLED = 1
      ## Enables additional recognition of color barcodes on color images.</p>
      ENABLED = 2


class BarcodeQualityMode(Enum):
      """!
      Mode which enables methods to recognize barcode elements with the selected quality. Barcode element with lower quality requires more hard methods which slows the recognition.
      \code
         reader = Recognition.BarCodeReader(self.image_path_code39, None,[Recognition.DecodeType.CODE_39_FULL_ASCII, Recognition.DecodeType.CODE_128])
        reader.getQualitySettings().setBarcodeQuality(Recognition.BarcodeQualityMode.LOW)
        results = reader.readBarCodes()
        for result in results:
            print(f"\nBarCode Type: {result.getCodeTypeName()}")
            print(f"BarCode CodeText: {result.getCodeText()}")
      \endcode
      """
      ## Enables recognition methods for High quality barcodes.</p>
      HIGH = 0

      ## Enables recognition methods for Common(Normal) quality barcodes.</p>
      NORMAL = 1
      ## Enables recognition methods for Low quality barcodes.</p>
      LOW = 2