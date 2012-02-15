class Project
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, :type => String
  field :path, :type => String
  field :created_by, :type => String

  has_many :groups
end
