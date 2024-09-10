depends = ('ITKPyBase', 'ITKDistanceMap', 'ITKCommon', 'ITKCommon', 'ITKBinaryMathematicalMorphology', )
templates = (  ('FixTopologyBase', 'itk::FixTopologyBase', 'itkFixTopologyBaseISS3', True, 'itk::Image< signed short,3 >,itk::Image< signed short,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyBase', 'itk::FixTopologyBase', 'itkFixTopologyBaseIUC3', True, 'itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyBase', 'itk::FixTopologyBase', 'itkFixTopologyBaseIUS3', True, 'itk::Image< unsigned short,3 >,itk::Image< unsigned short,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveInside', 'itk::FixTopologyCarveInside', 'itkFixTopologyCarveInsideISS3', True, 'itk::Image< signed short,3 >,itk::Image< signed short,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveInside', 'itk::FixTopologyCarveInside', 'itkFixTopologyCarveInsideIUC3', True, 'itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveInside', 'itk::FixTopologyCarveInside', 'itkFixTopologyCarveInsideIUS3', True, 'itk::Image< unsigned short,3 >,itk::Image< unsigned short,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveOutside', 'itk::FixTopologyCarveOutside', 'itkFixTopologyCarveOutsideISS3', True, 'itk::Image< signed short,3 >,itk::Image< signed short,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveOutside', 'itk::FixTopologyCarveOutside', 'itkFixTopologyCarveOutsideIUC3', True, 'itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >,itk::Image< unsigned char,3 >'),
  ('FixTopologyCarveOutside', 'itk::FixTopologyCarveOutside', 'itkFixTopologyCarveOutsideIUS3', True, 'itk::Image< unsigned short,3 >,itk::Image< unsigned short,3 >,itk::Image< unsigned char,3 >'),
)
factories = ()
