class Element
  include MongoMapper::Document

  key :elclass, String
  key :eltype, String
  key :elname, String
  key :created_by, String
#  key :created_at, Integer
  timestamps!

  belongs_to :asset
#  many :elclasses
  many :versions
end
