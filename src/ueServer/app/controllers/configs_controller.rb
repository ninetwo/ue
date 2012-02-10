class ConfigsController < ApplicationController
  def show
    @config = Ueconfig.first(:proj    => params[:project],
                             :grp     => params[:group],
                             :asst    => params[:asset],
                             :elclass => params[:elclass],
                             :eltype  => params[:eltype],
                             :elname  => params[:elname])

    respond_to do |format|
      format.html
      format.json { render :json => @config }
    end
  end

  def create
    @config = Ueconfig.new(:proj    => params[:project],
                           :grp     => params[:group],
                           :asst    => params[:asset],
                           :elclass => params[:elclass],
                           :eltype  => params[:eltype],
                           :elname  => params[:elname],
                           :config  => params[:config])

    respond_to do |format|
      if @config.save
        format.html
        format.json { render :json => @config,
                      :status => :created }
      else
        format.html
        format.json { render :json => @config.errors,
                      :status => :unprocessable_entity }
      end
    end
  end

  def update
    @config = Ueconfig.first(:proj    => params[:project],
                             :grp     => params[:group],
                             :asst    => params[:asset],
                             :elclass => params[:elclass],
                             :eltype  => params[:eltype],
                             :elname  => params[:elname])

    if params[:config] != nil
      @config.config = params[:config]
    end

    respond_to do |format|
      if @config.update_attributes
        format.html
        format.json { head :no_content }
      else
        format.html
        format.json { render :json => @config.errors,
                      :status => :unprocessable_entity }
      end
    end
  end
end
