class Project
  include MongoMapper::Document

  key :name, String
  key :path, String
  key :created_by, String
  timestamps!

  many :groups
end
