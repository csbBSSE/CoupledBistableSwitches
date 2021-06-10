
This folder contains the codes used to analyse the RACIPE simulation data. 

# Pipeline

The scripts must be run in the following order in order to generate all the necessary files. The Master\_Parallel\_Pipelin.py script is based on the pipeline described here with an added functionality of running large number of RACIPE simulations parallely.
The commands to be run are described in the following format:
Order No. - Name of script / Command to be run - Location / dicrectory in which it is run.

Note: &ldquo;Replicate&rdquo; directory means the individual replicate folders of RACIPE simulations. &ldquo;Master&rdquo; directory refers to the folder containing all the three &ldquo;Replicate&rdquo; directories of a particular network.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">Sl.No.</th>
<th scope="col" class="org-left">Command / Script</th>
<th scope="col" class="org-left">Location</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-left">Steady_state_count.py</td>
<td class="org-left">Replicate</td>
</tr>


<tr>
<td class="org-right">2</td>
<td class="org-left">Multistable_counter_bimodality_calc.py</td>
<td class="org-left">Replicate</td>
</tr>


<tr>
<td class="org-right">3</td>
<td class="org-left">cat /1/msct.txt /2/msct.txt /3/msct.txt &gt; MS.txt</td>
<td class="org-left">Master</td>
</tr>


<tr>
<td class="org-right">4</td>
<td class="org-left">cat /1/sts.txt /2/sts.txt /3/sts.txt &gt; St.txt</td>
<td class="org-left">Master</td>
</tr>


<tr>
<td class="org-right">4</td>
<td class="org-left">cat /1/bmc.txt /2/bmc.txt /3/bmc.txt &gt; BC.txt</td>
<td class="org-left">Master</td>
</tr>


<tr>
<td class="org-right">5</td>
<td class="org-left">Steady\_state\_Master\_Compile.py</td>
<td class="org-left">Master</td>
</tr>


<tr>
<td class="org-right">6</td>
<td class="org-left">steady_state_csv_compile.py</td>
<td class="org-left">Master</td>
</tr>
</tbody>
</table>

This order of scripts will generate all the files used in the analysis of the resutls. However, to obtain excel files for ease of use other commands need to be run which are explained in the Master\_Parallel\_Pipeline.py script.

