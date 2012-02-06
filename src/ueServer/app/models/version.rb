class Version
  include MongoMapper::EmbeddedDocument

  key :version, Integer
  key :created_by, String
#  key :created_at, Integer
  timestamps!

#  belongs_to :element
end
