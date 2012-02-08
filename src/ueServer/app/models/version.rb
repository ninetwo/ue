class Version
  include MongoMapper::EmbeddedDocument

  key :version, Integer
  key :created_by, String
  timestamps!
end
