class Group
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, :type => String
  field :path, :type => String
  field :created_by, :type => String

  belongs_to :project
  has_many :assets

  def Group.get_group(project, group)
    p = Project.get_project(project)
    if p == {} || p == nil
      return {}
    else
      g = p.groups.where(:name => group).first
      if g == nil
        return {}
      else
        return g
      end
    end
  end

  def Group.get_groups(project)
    p = Project.get_project(project)
    if p == {} || p == nil
      return []
    else
      return p.groups
    end
  end
end
