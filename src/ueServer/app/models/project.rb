class Project
  include MongoMapper::Document

  key :name, String
  key :path, String
  timestamps!

  many :groups
end
