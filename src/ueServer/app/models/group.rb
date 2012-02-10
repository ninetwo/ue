class Group
  include MongoMapper::Document

  key :name, String
  key :path, String
  key :created_by, String
  timestamps!

  belongs_to :project
  many :assets
end
