class Project
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, :type => String
  field :path, :type => String
  field :created_by, :type => String

  has_many :groups

  def Project.get_project(project)
    p = Project.where(:name => project).first
    if p == nil
      return {}
    else
      return p
    end
  end
end
