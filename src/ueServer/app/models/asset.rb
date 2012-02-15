class Asset
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, :type => String
  field :path, :type => String
  field :created_by, :type => String

  belongs_to :group
  has_many :elements
end
