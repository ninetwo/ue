class Element
  include Mongoid::Document
  include Mongoid::Timestamps

  field :elclass, :type => String
  field :eltype, :type => String
  field :elname, :type => String
  field :created_by, :type => String

  belongs_to :asset
  embeds_many :versions
end
