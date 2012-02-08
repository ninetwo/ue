class Ueconfig
  include MongoMapper::Document

  key :proj, String
  key :grp, String
  key :asst, String
  key :elclass, String
  key :eltype, String
  key :elname, String
  timestamps!
end
