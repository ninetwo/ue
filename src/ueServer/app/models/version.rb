class Version
  include Mongoid::Document
  include Mongoid::Timestamps

  field :version, :type => Integer
  field :created_by, :type => String

  embedded_in :element
end
