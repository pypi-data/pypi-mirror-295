_E='absolute_error_max'
_D='absolute_error_min'
_C='relative_error_max'
_B='relative_error_min'
_A='relative_vs_absolute_min'
THRESHOLDS={_A:1e-12,_B:.001,_C:.01,_D:1e-07,_E:1e-06}
def get_thresholds(thresholds):A={};A.update(THRESHOLDS);A.update(thresholds);return A
class CompareValues:
	def __init__(A,dict_thresholds):B=dict_thresholds;A.relative_vs_absolute_min=B[_A];A.relative_error_min=B[_B];A.relative_error_max=B[_C];A.absolute_error_min=B[_D];A.absolute_error_max=B[_E]
	def calculate(A,test,reference):
		K='absolute';J='relative';I='warning';H='message';G='error_type';E=test;D=reference;C='error';F=-1 if E-D<0 else 1
		if abs(E)>A.relative_vs_absolute_min and D!=0:
			B=abs(E-D)/abs(D)
			if B<A.relative_error_max:
				if B>A.relative_error_min:return I,{C:F*B,G:J,H:f"Rel. err. > {A.relative_error_min} and < {A.relative_error_max}"}
			else:return C,{C:F*B,G:J,H:f"Rel. err. > {A.relative_error_max}"}
		else:
			B=abs(E-D)
			if B<A.absolute_error_max:
				if B>A.absolute_error_min:return I,{C:F*B,G:K,H:f"Abs. err. > {A.absolute_error_min} and < {A.absolute_error_max}"}
			else:return C,{C:F*B,G:K,H:f"Abs. err. > {A.absolute_error_max}"}
		return None,None