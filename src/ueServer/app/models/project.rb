class Project
  include MongoMapper::Document

  key :name, String
  key :path, String
  key :created_by, String
  key :created_at, Float

  many :groups
end
