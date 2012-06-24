require 'ue_file_utils'

include UeFileUtils

class Element
  include Mongoid::Document
  include Mongoid::Timestamps

  field :elclass,    :type => String
  field :eltype,     :type => String
  field :elname,     :type => String
  field :path,       :type => String
  field :created_by, :type => String

  belongs_to :asset
  embeds_many :versions

  before_save do
    self.path = get_path
  end

  after_save do
    UeFileUtils::create_dir get_path
  end

  before_destroy do
    self.versions.destroy_all
    UeFileUtils::delete_dir self.path
  end

  def self.get_element project, group, asset, elclass, eltype, elname
    a = Asset.get_asset project, group, asset
    if a == {} || a.nil?
      {}
    else
      e = a.elements.where(:elclass => elclass, :eltype => eltype, :elname => elname).first
      if e.nil?
        {}
      else
        JSON.parse(a.to_json).to_hash.merge(JSON.parse(e.to_json).to_hash)
      end
    end
  end

  def self.get_elements project, group, asset
    a = Asset.get_asset project, group, asset
    if a == {} || a.nil?
      []
    else
      e = []
      for element in a.elements
        e[e.size] = JSON.parse(a.to_json).to_hash.merge(JSON.parse(element.to_json).to_hash)
      end
      e
    end
  end

  private

  def get_path
    if self.path.nil?
      UeFileUtils::get_element_path self.asset.path, self.elclass, self.eltype, self.elname
    else
      self.path
    end
  end
end
