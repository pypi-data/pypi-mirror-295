import numpy as np
import sys
from scipy.stats.stats import pearsonr
from scipy.stats import tukey_hsd
import matplotlib.pyplot as plt
import pandas as pd

class comstab(object):
	'''
	comstab is an python class that contains basic functions to apply the
	unified framework for partitioning the drivers of stability of ecological
	communities (Segrestin et al. 2024 Global Ecology and Biogeography, 10.1111/geb.13828.
	'''
	def __init__(self):
		#self.data = data
		#self.datashape = np.shape(data)
		self.colors =  plt.get_cmap('tab20').colors
	
	def partition(self,data, stamp=True):
		"""
		partition is a function used to partition the temporal coefficient of variation 
		of a community into the variability of the average species and three stabilizing 
		effects: the dominance, asynchrony and averaging effects
		data: is a matrix or an array containing the biomass timeseries of the species 
		in the community
		stamp: if True the results are printed on the screen
		RETURN: res a dictionary containing the following keys:
		- CVs: an array containing the coefficient of variation of the average species, 
		       the total variability of the community, the total variability of the community 
		       corrected for the asynchrony effect and the total variability of the community 
		       corrected for the asynchrony and averaging effects
		- Stabilization: an array containing the total stabilization of the community, the 
		                 dominance effect, the asynchrony effect and the averaging effect
		- Relative: an array containing the relative contributions of the dominance, asynchrony
					and averaging effects to the total stabilization of the community
		- Taylor: an array containing the slope and the intercept of the linear fit of the Taylor's power law and the p-value of the fit
		"""
		datashape = np.shape(data)
		#check if self.data is a matrix otherwise print error message
		if len(datashape) == 0:
			print("Error: data should be a matrix or array")
			sys.exit()
		#check if self.data element are all positive otherwise print error message
		if np.any(data < 0):
			print("Error: data should be positive")
			sys.exit()
		#number of species
		n = datashape[0]

		#compute the mean of the community (the biomass of the species are summed up)
		meansum = np.nanmean(np.nansum(data,axis=0))
		#compute the variance of the community
		varsum = np.nanvar(np.nansum(data,axis=0))
		#compute the coefficient of variation of the community
		cvsum = np.sqrt(varsum)/meansum

		if cvsum == 0:
			print("Error: The community CV is zero. This analysis does not apply to perfectly stable communities.")
			sys.exit()

		res = {
			"CVs": np.zeros(4),           # CVe, CVtilde, CVa, CVc
			"Stabilization": np.zeros(4), # tau, delta, psi, omega
			"Relative": np.zeros(3),       # delta_cont, psi_cont, omega_cont
			"Taylor": np.zeros(3)         # slope, intercept
		}

		#analysis is not relevant for a single species community
		if datashape[0] == 1:
			print("Warning: This analysis is not relevant for single-species communities. All stabilizing effects were fixed to 1.")
			res["CVs"] = np.array([cvsum,cvsum,cvsum,cvsum])
			res["Stabilization"] = np.array([1,1,1,1])
			res["Relative"] = np.array([np.nan,np.nan,np.nan])
			res["Taylor"] = np.array([np.nan,np.nan,np.nan])
			return res

		else:
			#compute the mean of each species
			meani = np.nanmean(data, axis=1)
			#compute the variance of each species
			vari = np.nanvar(data, axis=1)
			#compute the coefficient of variation of each species
			cvi = np.sqrt(vari)/meani

			#check if there are not fluctuating species
			if np.any(cvi == 0):
				print("Warning: Non-fluctuating species found in data, they will non be considered in the analysis")
				cvi[cvi == 0] = np.nan
				meani[cvi == 0] = np.nan

			#compute the taylor's law coefficient
			#linear fit of the log-log relationship between the coefficient of variation (y) and the mean (x) of the species
			TPL = np.polyfit(np.log10(meani[~np.isnan(meani)]), np.log10(cvi[~np.isnan(cvi)]), 1) #TPL[0] = b TPL[1] = a

			#test the significance of the fit with Pearson correlation and p value
			_, p = pearsonr(np.log10(meani[~np.isnan(meani)]), np.log10(cvi[~np.isnan(cvi)]))

#		plt.plot(np.log10(meani), np.log10(cvi), 'o')
#		plt.plot(np.log10(meani), np.polyval(TPL, np.log10(meani)))
#		plt.xlabel("log10(mean)")
#		plt.ylabel("log10(CV)")
#		plt.title("Taylor's law")
#		plt.show()
#		print("p-value: %.2f" % p)

			if p > 0.05:
				print("Error: The fit of Taylor's law is not significant, the analysis is not relevant.")
				sys.exit()

			#compute the coefficient of variation of the average species
			CVe = 10**TPL[1] * (meansum / n)**TPL[0]

			#Dominance effect
			sumsd = np.nansum(np.sqrt(vari))
			CVtilde = sumsd / meansum
			Delta = CVtilde / CVe

			if Delta > 1:
				print("Warning: Destabilizing effect of dominants. Relative effects cannot be computed.")

			#Compensatory dynamics
			sdsum = np.sqrt(varsum)
			rootPhi = sdsum /sumsd

			#Asynchrony effect
			sumvar = np.nansum(vari)
			beta = np.log10(1/2) / ( np.log10(sumvar / (sumsd**2) ) )
			Psi = rootPhi**beta

			#Averaging effect
			omega = rootPhi / Psi

			if omega >1:
				print("Warning: Community diversity is lower than the null diversity. Relative effects cannot be computed.")

			#Total stabilization
			tau = Delta * Psi * omega

			#Outputs
			res["CVs"] = np.array([CVe, CVtilde, CVtilde*Psi, cvsum])
			res["Stabilization"] = np.array([tau, Delta, Psi, omega])
			res["Taylor"] = np.array([(TPL[0]+1)*2,TPL[1],p])

			#Relative effects
			if res["Stabilization"].max() > 1:
				res["Relative"] = np.array([np.nan,np.nan,np.nan])
			else:
				res["Relative"] = np.array([np.log10(Delta)/np.log10(tau), np.log10(Psi)/np.log10(tau), np.log10(omega)/np.log10(tau)])
			
			if stamp:
				print("Partitionning of the community temporal variability (CV)")
				print("Community CV: %.2f" % cvsum)
				print("Total stabilisation: %.2f" % tau)
				print("Dominance effect: %.2f" % Delta)
				print("Asynchrony effect: %.2f" % Psi)
				print("Averaging effect: %.2f" % omega)
				print("Relatives contributions:")
				print("Dominance: %.2f" % res["Relative"][0])
				print("Asynchrony: %.2f" % res["Relative"][1])
				print("Averaging: %.2f" % res["Relative"][2])
			return res
		
	def ternaryplot(self,res,tau=None,color=None,coloraxes=True,figname='ternary.png',sizelegend=False,marker=None,labels=None):
		'''
		ternaryplot() is a graph function used to represent the relative contributions
		of the three stabilizing effects ("Dominance", "Asynchrony" and "Averaging") on a
		ternary plot.
		rel:        is an array containing the relative contributions of the three stabilizing
		            or a matrix Nx3 where each rows contains the relative contributions for 
			        different N communities
		tau:        array of total stabilization, it is used as reference for the size of
		            the point in the ternary plot when more communities are studie, if None all the points will have the same size
		color:      string or array of N string, color of the point(s) in the ternary plot associated
		 	        to each of the community or the N communities studied
			        if None it uses tab20 color palette
		coloraxes:  True -> axes and grid are colored otherwise are in black
		figname:    name of the figure where to save the plot, default is ternary.png
		sizelegend: if True a legend showing the relationship between the total
		            stabilization and the size of point is displayed
		marker:     default None, if not None the marker of the plot is set to the string of marker,
			        if an array of markers is provided, each community wiil be plotted with the relative marker
		labels:     default None, if not None the labels of the points are set to the string of labels,
					should specifiy the name of the communities and have dimension N
		RETURN: fig,ax figure and axes where the plot is constructed
		'''
		import mpltern
		from matplotlib.ticker import MultipleLocator
		if len(np.shape(color)) == 0:
			color = np.array([color])
		
		if (color == None).any():
		#if len(color) == 0:
				color = np.array(self.colors)

		fig = plt.figure(figsize=(9, 6))
		ax = fig.add_subplot(projection='ternary')

		#check if res is an array or matrix
		if len(np.shape(res)) == 1:
			res = np.array([res])
		
		if np.shape(res)[1] != 3:
			print("Error: res should have 3 columns, one for each relative contribution")
			sys.exit()
		#check if tau and res have consistent dimennsions
		if tau.any() != None:
			#check if tau is a value or an array
			if not hasattr(tau, "__len__"):
				tau = np.array([tau])
			if np.shape(tau)[0] != np.shape(res)[0]:
				print("Error: tau and res should have the same number of rows")
				sys.exit()

		#check if labels is an array
		if len(np.shape(labels)) == 0:
				labels = np.array([labels])
		#if it is a list make it an array
		if type(labels) == list:
			labels = np.array(labels)

		#loop over the communities
		for irel, rel in enumerate(res):
			if tau.any() == None:
				if marker == None:
					ax.scatter(rel[1], rel[0], rel[2], color=color[irel],label=labels[irel])
				else:
					if len(np.shape(marker)) == 0:
						marker = np.array([marker])
					ax.scatter(rel[1], rel[0], rel[2], color=color[irel], marker=marker[irel],label=labels[irel])
			else:
				if (marker == None).any():
					ax.scatter(rel[1], rel[0], rel[2], color=color[irel], s=tau[irel]*300+10,label=labels[irel])
				else:
					if len(np.shape(marker)) == 0:
						marker = np.array([marker])
					ax.scatter(rel[1], rel[0], rel[2], color=color[irel], marker=marker[irel], s=tau[irel]*300+10,label=labels[irel])
	
			ax.taxis.set_major_locator(MultipleLocator(0.20))
			ax.laxis.set_major_locator(MultipleLocator(0.20))
			ax.raxis.set_major_locator(MultipleLocator(0.20))
			#ax.grid()
	
			#axis label if arrows are not used
			#ax.set_tlabel('Asynchrony contribution $\psi_{rel}$')
			#ax.set_llabel('Dominance contribution $\delta_{rel}$')
			#ax.set_rlabel('Averaging contribution $\omega_{rel}$')
	
			#ax.taxis.set_label_position('tick1')
			#ax.laxis.set_label_position('tick1')
			#ax.raxis.set_label_position('tick1')
	
			ax.tick_params(labelrotation="horizontal")
	
			#arrows along axis
			from matplotlib.patches import ArrowStyle, FancyArrowPatch
			arrowstyle = ArrowStyle('simple', head_length=10, head_width=5)
			kwargs_arrow = {
	    		'transform': ax.transAxes,  # Used with ``ax.transAxesProjection``
	    		'arrowstyle': arrowstyle,
	    		'linewidth': 1,
	    		'clip_on': False,  # To plot arrows outside triangle
	    		'zorder': -10,  # Very low value not to hide e.g. tick labels.
			}
	
			# Start of arrows in barycentric coordinates.
			ta = np.array([ 0.1, -0.1,  1.1])
			la = np.array([ 1.1,  0.0, -0.1])
			ra = np.array([-0.1,  1.1,  0.0])
	
			# End of arrows in barycentric coordinates.
			tb = np.array([ 1.0, -0.1,  0.1])
			lb = np.array([ 0.1,  1.0, -0.1])
			rb = np.array([-0.1,  0.1,  1.0])
	
			# This transforms the above barycentric coordinates to the original Axes
			# coordinates. In combination with ``ax.transAxes``, we can plot arrows fixed
			# to the Axes coordinates.
			f = ax.transAxesProjection.transform

			if coloraxes:
				tarrow = FancyArrowPatch(f(ta), f(tb), ec='#E69F00', fc='#E69F00', **kwargs_arrow)
				larrow = FancyArrowPatch(f(la), f(lb), ec='#56B4E9', fc='#56B4E9', **kwargs_arrow)
				rarrow = FancyArrowPatch(f(ra), f(rb), ec='#009E73', fc='#009E73', **kwargs_arrow)
			else:
				tarrow = FancyArrowPatch(f(ta), f(tb), ec='k', fc='k', **kwargs_arrow)
				larrow = FancyArrowPatch(f(la), f(lb), ec='k', fc='k', **kwargs_arrow)
				rarrow = FancyArrowPatch(f(ra), f(rb), ec='k', fc='k', **kwargs_arrow)
			ax.add_patch(tarrow)
			ax.add_patch(larrow)
			ax.add_patch(rarrow)
	
			# To put the axis-labels at the positions consistent with the arrows above, it
			# may be better to put the axis-label-text directly as follows rather than
			# using e.g.  ax.set_tlabel.
			kwargs_label = {
	    		'transform': ax.transTernaryAxes,
	    		'backgroundcolor': 'w',
	    		'ha': 'center',
	    		'va': 'center',
	    		'rotation_mode': 'anchor',
	    		'zorder': -9,  # A bit higher on arrows, but still lower than others.
			}
	
			# Put axis-labels on the midpoints of arrows.
			tpos = (ta + tb) * 0.5
			lpos = (la + lb) * 0.5
			rpos = (ra + rb) * 0.5
	
			ax.text(*tpos, r'Asynchrony contribution $\psi_{rel}$'  , color='k', rotation=-60, **kwargs_label)
			ax.text(*lpos, r'Dominance contribution $\Delta_{rel}$' , color='k', rotation= 60, **kwargs_label)
			ax.text(*rpos, r'Averaging contribution $\omega_{rel}$', color='k', rotation=  0, **kwargs_label)

		plt.subplots_adjust(right=0.9)
		ax.grid(visible=True)

		#show legend of communities names
		flag = True
		for ll in labels:
			if ll == None:
				flag = False
		if flag:
			legend1 = ax.legend(loc='lower left',frameon=False,ncol=3,bbox_to_anchor=(0.8,0.6),title='Communities')
			#use plt.gca().add_artist(legend1) to add the legend but move it to the upper right of the figure
			plt.gca().add_artist(legend1)

		if coloraxes :
			# Color ticks, grids, tick-labels
			ax.taxis.set_tick_params(tick2On=True, colors='#E69F00', grid_color='#E69F00')
			ax.laxis.set_tick_params(tick2On=True, colors='#56B4E9', grid_color='#56B4E9')
			ax.raxis.set_tick_params(tick2On=True, colors='#009E73', grid_color='#009E73')

			# Color labels
			ax.taxis.label.set_color('#E69F00')
			ax.laxis.label.set_color('#56B4E9')
			ax.raxis.label.set_color('#009E73')

			# Color spines
			ax.spines['tside'].set_color('#E69F00')
			ax.spines['lside'].set_color('#56B4E9')
			ax.spines['rside'].set_color('#009E73')
		
		if sizelegend:
			gll = ax.scatter([],[],[], s=0.1*300+10, marker='o', color='#555555')
			gl = ax.scatter([],[],[], s=0.4*300+10, marker='o', color='#555555')
			ga = ax.scatter([],[],[], s=0.7*300+10, marker='o', color='#555555')
			gb = ax.scatter([],[],[], s=1.0*300+10, marker='o', color='#555555')

			ax.legend((gll,gl,ga,gb),
				('0.1', '0.4', '0.7', '1.0'),
				scatterpoints=1,
				loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
				title='Total\nStabilization',
				borderpad=1.5,
				bbox_to_anchor=(0.97,0.35))
			
		
		fig.tight_layout()
		fig.savefig(figname,dpi=600)
		plt.plot()
		return fig,ax

	def plotCV(self,CV_arr,color=None,figname='CVs.png',ylogscale=True,ylabel=None,marker=None,errorbar=np.array([None]),labels=None):
		'''
		Function plotting the impacts on CV by dominance, asynchrony and averaging
		CV_arr:    array or matrix containinf the CVs computed by the partition function,
		           it has 4 columns and N rows as the N communities studied
		color:     string or array of N string, color of the point(s) in the plot associated
		 	       to each of the community or the N communities studied, if not give tab20 is used
		figname:   name of the figure where to save the plot
		ylogscale: if True the y-axis is in log scale, default True
		ylabel:    default None, if not None the y-axis label is set to the string of ylabel
		marker:    default None, if not None the marker of the plot is set to the string of marker,
			       if an array of markers is provided, each community wiil be plotted with the relative marker
		errorbar:  default None, if not None the errorbar of the plot is set to the value of errorbar,
				   if an array of errorbars is provided, each community wiil be plotted with the relative errorbar
				   should have the same dimensions of CV_arr
		labels:    default None, if not None the labels of the points are set to the string of labels,
				   should specifiy the name of the communities and have dimension N
		RETURN: fig,ax figure and axes where the plot is constructed
		'''

		if len(np.shape(color)) == 0:
			color = np.array([color])
		
		if (color == None).any():
				color = np.array(self.colors)
	
		fig = plt.figure(figsize=(6, 6))
		ax = fig.add_subplot()

		
		#check if CV is an array or matrix
		if len(np.shape(CV_arr)) == 1:
				CV_arr = np.array([CV_arr])
		
		if np.shape(CV_arr)[1] != 4:
			print("Error: CV should have 4 columns, one for each CV")
			sys.exit()
		
		#check if errorbar is an array
		if len(np.shape(errorbar)) == 0:
				errorbar = np.array([errorbar])
		if errorbar.any() != None:
			#check if errorbar is an array or matrix
			if len(np.shape(errorbar)) == 1:
				errorbar = np.array([errorbar])
			#chek if errorbar has the same dimensions of CV_arr
			if np.shape(errorbar) != np.shape(CV_arr):
				print("Error: errorbar should have the same dimensions of CV_arr")
				sys.exit()		

		#check if labels is an array
		if len(np.shape(labels)) == 0:
				labels = np.array([labels])

		#loop over the communities
		if (marker == None).any():
			for icv, cv in enumerate(CV_arr):
				if errorbar.any() == None:
					ax.plot(np.arange(4), cv, color=color[icv], marker='o', markersize=10, alpha=0.5, label=labels[icv])
				else:
					ax.errorbar(np.arange(4), cv, yerr=errorbar[icv], ls='-', fmt='o', color=color[icv], markersize=10, alpha=0.5, label=labels[icv])
		else:
			if len(np.shape(marker)) == 0:
				marker = np.array([marker])
			for icv, cv in enumerate(CV_arr):
				if errorbar.any() == None:
					ax.plot(np.arange(4), cv, color=color[icv], marker=marker[icv], markersize=10, alpha=0.5, label=labels[icv])
				else:
					ax.errorbar(np.arange(4), cv, yerr=errorbar[icv], ls='-', fmt=marker[icv], color=color[icv], markersize=10, alpha=0.5, label=labels[icv])
		#set the xticks to the name of the CVs
		ax.set_xticks(np.arange(4))
		ax.set_xticklabels(['$CV_e$',r'$\widetilde{CV}$','$CV_a$','$CV_c$'])

		#put     text $
		# ù+Delta$ in the plot, between the first two ticks of the x-axis , with the same font size of ticks
		ax.text(0.18,0.02,r'$\Delta$',transform=ax.transAxes,fontsize=12)
		ax.text(0.50,0.02,r'$\psi$',transform=ax.transAxes,fontsize=12)
		ax.text(0.80,0.02,r'$\omega$',transform=ax.transAxes,fontsize=12)
		if ylogscale:
			ax.set_yscale('log')
		plt.gca().get_yaxis().clear() #removes the y-axis ticks to set the new ones

		#set y ticks and tickslabes to 0.2,0.4,0.6,0.8,1.0
		ax.set_yticks([0.2,0.4,0.6,0.8,1.0])
		ax.set_yticklabels(['0.2','0.4','0.6','0.8','1.0'])

		if ylabel != None:
			ax.set_ylabel(ylabel)
		
		#show legend of communities names
		flag = True
		for ll in labels:
			if ll == None:
				flag = False
		if flag:
			legend1 = ax.legend(loc='upper right',frameon=False,ncol=3)
			plt.gca().add_artist(legend1)


		fig.tight_layout()

		fig.savefig(figname,dpi=600)
	
		return fig,ax
	
	def plotEFFECT(self,EFF,color=None,figname='effect.png',ylogscale=False,ylabel='Stabilisation',marker=None,errorbar=np.array([None]),labels=None,legend=False):
		'''
		Function plotting the dominance, asynchrony and averaging effects for different communities in three subplots
		EFF:       array or matrix containing the effects of each stabilisation element computed by the partition
		           function, it has 3 columns and N rows as the N communities studied
		color:     string or array of N string, color of the point(s) in the plot associated
		 	       to each of the community or the N communities studied, if not give tab20 is used
		figname:   name of the figure where to save the plot, default is effect.png
		ylogscale: if True the y-axis is in log scale, default False
		ylabel:    default 'Stabilisation', if  None it is removed, it is showd only on leftmost plot
		marker:    default None, if not None the marker of the plot is set to the string of marker,
			       if an array of markers is provided, each community wiil be plotted with the relative marker
		errorbar:  default None, if not None the errorbar of the plot is set to the value of errorbar,
				   if an array of errorbars is provided, each community wiil be plotted with the relative errorbar
				   should have the same dimensions of EFF
		labels:    default None, if not None the labels of the points are set to the string of labels,
				   should specifiy the name of the communities and have dimension N
		RETURN: fig,ax figure and axes where the plot is constructed
		'''

		if len(np.shape(color)) == 0:
			color = np.array([color])
		
		if (color == None).any():
				color = np.array(self.colors)
	
		fig = plt.figure(figsize=(15, 4))
		#add 3 subplots on the same row
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)

		
		#check if EFF is an array or matrix
		if len(np.shape(EFF)) == 1:
				EFF = np.array([EFF])
		
		if np.shape(EFF)[1] != 3:
			print("Error: EFF should have 3 columns, one for each effect")
			sys.exit()
		
		#number of communities
		N = np.shape(EFF)[0]

		#check if errorbar is an array
		if len(np.shape(errorbar)) == 0:
				errorbar = np.array([errorbar])
		if errorbar.any() != None:
			#check if errorbar is an array or matrix
			if len(np.shape(errorbar)) == 1:
				errorbar = np.array([errorbar])
			#chek if errorbar has the same dimensions of EFF
			if np.shape(errorbar) != np.shape(EFF):
				print("Error: errorbar should have the same dimensions of EFF")
				sys.exit()		

		#check if labels is an array
		if len(np.shape(labels)) == 0:
				labels = np.array([labels])

		#loop over the communities
		if (marker == None).any():
			for icv, cv in enumerate(CV_arr):
				if errorbar.any() == None:
					ax1.scatter(icv, EFF[icv,0], color=color[icv], marker='o',alpha=0.5, label=labels[icv])
					ax2.scatter(icv, EFF[icv,1], color=color[icv], marker='o',alpha=0.5, label=labels[icv])
					ax3.scatter(icv, EFF[icv,2], color=color[icv], marker='o',alpha=0.5, label=labels[icv])
				else:
					ax1.errorbar(icv, EFF[icv,0], yerr=errorbar[icv,0], fmt='o', color=color[icv],alpha=0.5, label=labels[icv])
					ax2.errorbar(icv, EFF[icv,1], yerr=errorbar[icv,1], fmt='o', color=color[icv],alpha=0.5, label=labels[icv])
					ax3.errorbar(icv, EFF[icv,2], yerr=errorbar[icv,2], fmt='o', color=color[icv],alpha=0.5, label=labels[icv])
		else:
			if len(np.shape(marker)) == 0:
				marker = np.array([marker])
			for icv, cv in enumerate(EFF):
				if errorbar.any() == None:
					ax1.scatter(icv, EFF[icv,0], color=color[icv], marker=marker[icv],alpha=0.5, label=labels[icv])
					ax2.scatter(icv, EFF[icv,1], color=color[icv], marker=marker[icv],alpha=0.5, label=labels[icv])
					ax3.scatter(icv, EFF[icv,2], color=color[icv], marker=marker[icv],alpha=0.5, label=labels[icv])
				else:
					ax1.errorbar(icv, EFF[icv,0], yerr=errorbar[icv,0], fmt=marker[icv], color=color[icv],alpha=0.5, label=labels[icv])
					ax2.errorbar(icv, EFF[icv,1], yerr=errorbar[icv,1], fmt=marker[icv], color=color[icv],alpha=0.5, label=labels[icv])
					ax3.errorbar(icv, EFF[icv,2], yerr=errorbar[icv,2], fmt=marker[icv], color=color[icv],alpha=0.5, label=labels[icv])
		#set the xticks to the name of the number of communities studied
		ax1.set_xticks(np.arange(N))
		ax1.set_xticklabels(labels)
		ax2.set_xticks(np.arange(N))
		ax2.set_xticklabels(labels)
		ax3.set_xticks(np.arange(N))
		ax3.set_xticklabels(labels)


		if ylogscale:
			ax1.set_yscale('log')
			ax2.set_yscale('log')
			ax3.set_yscale('log')
			print("Warning: y-axis is in symlog scale")
		

		#set y lim to [0.,1.]
		ax1.set_ylim([0.05,1.5])
		ax2.set_ylim([0.05,1.5])
		ax3.set_ylim([0.05,1.5])

		#set y ticks and tickslabes to 0.2,0.4,0.6,0.8,1.0, show only on leftmost plot
		ax1.set_yticks([0.2,0.4,0.6,0.8,1.0])
		ax1.set_yticklabels(['0.2','0.4','0.6','0.8','1.0'])
		ax2.set_yticks([0.2,0.4,0.6,0.8,1.0])
		ax2.set_yticklabels([])
		ax3.set_yticks([0.2,0.4,0.6,0.8,1.0])
		ax3.set_yticklabels([])

		#horizontal line in ax1 at y=1
		ax1.axhline(y=1, color='k', linestyle='--',alpha=0.5)
		#horizontal line in ax2 at y=np.sqrt(1/2)
		ax2.axhline(y=np.sqrt(1/2), color='k', linestyle='--',alpha=0.5)
		

		if ylabel != None:
			ax1.set_ylabel(ylabel)
		
		#show legend of communities names
		if legend:
			ax1.legend(loc='upper right',frameon=False)

		#add title to each subplot
		ax1.set_title(r'Dominance effect $\Delta$')
		ax2.set_title(r'Asynchrony effect $\psi$')
		ax3.set_title(r'Averaging effect $\omega$')

		fig.tight_layout()

		fig.savefig(figname,dpi=600)
	
		return fig,(ax1,ax2,ax3)
	
	def Tukey(self,data,labels=None,savecsv=False,csvname='Tukey.csv'):
		'''
		function to perform the Tukey's test on the data
		Inputs:  
		data:	 matrix of shape NxM, where N is the number of groups and M the number of samples
		labels:  list of N strings containing the name of the groups, deault is None
		savecsv: if True the results are saved in a csv file, default is False
		csvname: name of the csv file where to save the results, default is Tukey.csv
		Returns: pandas dataframe with the p-values of the Tukey's test, 
				 diagonal is ones as the comparison is with itself, the matrix is symmetric
		'''
		#check if data is a matrix
		if len(np.shape(data)) == 0:
			print("Error: data should be a matrix")
			sys.exit()
		#divide the data in N groups
		#create N arrays long M
		N = np.shape(data)[0]

		if (labels == None).any():
			labels = np.arange(N)
		#label mask to remove nans
		mask = np.array([True]*N)
		arrays_dict = {}
		for i in range(N):
			arrays_dict[f'data{i}'] = data[i]
			#drop nans from the arrays
			arrays_dict[f'data{i}'] = arrays_dict[f'data{i}'][~np.isnan(arrays_dict[f'data{i}'])]
			#if one array is empty remove from the dictionary
			if len(arrays_dict[f'data{i}']) == 0 or len(arrays_dict[f'data{i}']) == 1:
				arrays_dict.pop(f'data{i}')
				print(f"Warning: {labels[i]} is empty and was removed")
				mask[i] = False
		#remove the labels that have been removed
		labels = labels[mask]
		
		arrays_list = list(arrays_dict.values())

		#compute the Tukey's test
		pvalues = tukey_hsd(*arrays_list).pvalue

		#load pvlaues in a pandas dataframe
		
		df = pd.DataFrame(pvalues, columns=labels, index=labels)

		#save the results in a csv file
		if savecsv:
			df.to_csv(csvname)

		return df
