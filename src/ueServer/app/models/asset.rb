class Asset
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, :type => String
  field :path, :type => String
  field :created_by, :type => String

  belongs_to :group
  has_many :elements

  def Asset.get_asset(project, group, asset)
    g = Group.get_group(project, group)
    if g == {} || g == nil
      return {}
    else
      a = g.assets.where(:name => asset).first
      if a == nil
        return {}
      else
        return a
      end
    end
  end

  def Asset.get_assets(project, group)
    g = Group.get_group(project, group)
    if g == {} || g == nil
      return []
    else
      return g.assets
    end
  end
end
