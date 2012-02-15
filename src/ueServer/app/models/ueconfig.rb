class Ueconfig
  include Mongoid::Document
  include Mongoid::Timestamps

  field :proj, :type => String
  field :grp, :type => String
  field :asst, :type => String
  field :elclass, :type => String
  field :eltype, :type => String
  field :elname, :type => String
end
