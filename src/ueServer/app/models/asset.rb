class Asset
  include MongoMapper::Document

  key :name, String
  key :path, String
  timestamps!

  belongs_to :group
  many :elements
end
