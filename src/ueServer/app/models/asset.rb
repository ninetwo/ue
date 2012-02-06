class Asset
  include MongoMapper::Document

  key :name, String
  key :path, String
  key :created_by, String
  key :created_at, Integer

  belongs_to :group
  many :elements
end
